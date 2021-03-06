from datetime import datetime
import os
from time import time
import threading
import fileinput
import sys

from variables import *

#    T I M E  &  D A T E 
#    #    #    #    #    #    #    #    #   #
#
# find week number from timestamp
def ts_to_week(time_stamp):
    i = 1
    week = day1
    in_week = False
    while not in_week:
        in_week = (time_stamp >= week and time_stamp <= week + one_week)
        if in_week:
            return i
        week = week + one_week
        i += 1

# define time funtions
def get_current_time():
    return int(time())

def get_time_passed(start, end):
   return end - start

# function to convert timestamp to date 
def ts_to_date(time_stamp):
    return datetime.fromtimestamp(time_stamp).isoformat()

# turn a timestamp into hrs:mins:secs
def secs_to_hours(secs):
    one_hour = 60 * 60
    one_minute = 60

    mod_minutes = secs % one_hour

    hours = secs / one_hour
    hours = int(hours)

    seconds = mod_minutes % one_minute

    minutes = mod_minutes / one_minute
    hrs = str(hours)
    mins = '0' + str(int(minutes))
    secs = '0' + str(seconds)

    return hrs + ':' + mins[len(mins) - 2 : len(mins)] + ':' + secs[len(secs) - 2 : len(secs)]

def get_month():
    mydate = datetime.now()
    return mydate.strftime("%B %Y")


#    C L E A N I N G  F U N C T I O N S
#    #    #    #    #    #    #    #    #   #
#
# check if there is a temp file
def temp_file_opens():
    try:
        temp = open(l_s_temp)
        temp.close()
        return True
    except: 
        pass
    return False

def l_s_clean():
    if (temp_file_opens()):
        print 'temp file exists, attempting to copy file'
        try:
            print 'trying to clean temp file'
            temp = open(l_s_temp).read()
            target = open(l_s_path, 'w')
            target.truncate()
            target.write(temp)
            target.close()
            print 'file copied.. deleting temp file'
            os.remove(l_s_temp)
        except IOError: 
            print 'error cleaning up temp file..'
            raise


#    L A S T  S E S S I O N  R E A D 
#    #    #    #    #    #    #    #    #   #
#
# line..
# 0 -> total accumilated time
# 1 -> total forever accumilated time
# 2 -> last time stamp
# 3 -> last time stamp readable date
 
def l_s_read():
    return open(l_s_path).read()

def l_s_read_line(line):
    lines = open(l_s_path).readlines()
    return lines[line]

#    M O N T H  R E A D 
#    #    #    #    #    #    #    #    #   #
#
# perform a lookup for the first line that matches, the line below that
def total_for_month(month):
    with open(monthly_path) as monthly:
        return_next_line = False
        for line in monthly:
            line = line.strip()
            if return_next_line:
                return line
            if line == get_month():
                return_next_line = True
            


#    C O N V E R T  T O  S T R I N G 
#    #    #    #    #    #    #    #    #   #
#
# function to convert to string if necessary
def convert_to_string(input):
    if not (isinstance(input, basestring)):
        input = str(input)
    return input


#    L A S T  S E S S I O N  W R I T E 
#    #    #    #    #    #    #    #    #   #
#
# define file rewrite function
def re_write_l_s(total, forever_total, latest_ts, latest_readable):
    open(l_s_temp, 'w').write(l_s_read())
    new_file = open(l_s_path, 'w')
    new_file.truncate()
    total = convert_to_string(total)
    new_file.write(total + '\n')
    new_file.write(forever_total + '\n')
    new_file.write(str(latest_ts) + '\n')
    new_file.write(latest_readable + '\n' )
    os.remove(l_s_temp)


#    M O N T H L Y  W R I T E 
#    #    #    #    #    #    #    #    #   #
#
# go through the monthly file and find the correct line to change
# then loop through it again with a change on the desired line
# I know.. I should refactor it to one loop.. one day..
def write_monthly(new_total):
    # first find the monthly value to replace
    replace_line = None
    with open(monthly_path) as monthly:
        count = 1
        for line in monthly:
            if get_month() in line: 
                replace_line = count
                break
            count = count + 1
    
    if replace_line:
        for line in fileinput.input(monthly_path, inplace=True):
            line_num = fileinput.filelineno()
            if line_num == replace_line + 1:
                sys.stdout.write("%d\n" % new_total)
            else:
                sys.stdout.write(line)

    else:
        monthly = open(monthly_path, 'a')
        monthly.write(get_month() + '\n')
        monthly.write('%d\n' % new_total)
            
    
#    U P D A T E   T I M E R 
#    #    #    #    #    #    #    #    #   #
def update_l_s(update_stop):
    # update files here
    # re_write_l_s(sess.get_total_this_week())
    if not update_stop.is_set():
        threading.Timer(2, update_l_s, [update_stop]).start()
