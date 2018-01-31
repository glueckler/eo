#!/usr/bin/env python
print 'empty objects'
from time import time
import os
import threading
from datetime import datetime

day1 = 1517184000 + (8 * 60 * 60) # utc + 8 hours
one_week = 7 * 24 * 60 * 60

#
# find week number from timestamp
#
def ts_to_week(time_stamp):
    i = 1
    week = day1
    inWeek = False
    while not inWeek:
        inWeek = (time_stamp > week and time_stamp <= week + one_week)
        if inWeek:
            return i
        week = week + one_week
        i += 1

#
# last_session file functions
#
l_s_path = './last_session.py'
l_s_temp = './last_session_temp.py'

#
# function to convert timestamp to date 
#
def ts_to_date(time_stamp):
    return datetime.fromtimestamp(time_stamp).isoformat()

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
l_s_clean()


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

#
# function to convert to string if necessary
#
def convert_to_string(input):
    if not (isinstance(input, basestring)):
        input = str(input)
    return input

#
# define time funtions
#
def get_current_time():
    return int(time())

def get_time_passed(start, end):
   return end - start

#
# define file rewrite function
#
def re_write_l_s(total, forever_total, latest_ts, latest_readable):
    temp = open('./last_session_temp.py', 'w').write(l_s_read())
    new_file = open(l_s_path, 'w')
    new_file.truncate()
    total = convert_to_string(total)
    new_file.write(total + '\n')
    new_file.write(forever_total + '\n')
    new_file.write(str(day1) + '\n')
    new_file.write(ts_to_date(day1) + '\n' )
    os.remove(l_s_temp)

#
# define session class
#
class Session:
    def __init__(self, current_time):
        print 'initializing Session :)'
        self.active = True

        self.start_time = current_time

        self.total_this_week = int(l_s_read_line(0))
        self.total_forever = int(l_s_read_line(1))

        self.current_week = ts_to_week(self.start_time)

        self.latest_week = int(l_s_read_line(2))
        # self.is_same_week = ts_to_week(self.latest_week) == self.current_week

        print 'current week: week %d' % self.current_week
        print 'total time accumalated.. %d' % self.total_this_week

    def get_total_session_time(self):
        return get_time_passed(self.start_time, get_current_time())

    def get_total_this_week(self):
        return self.get_total_session_time() + self.total_this_week

    def write_l_s(self):
        sess_time = self.get_total_session_time()
        total_forever = str(self.total_forever + sess_time)
        latest_ts = str(self.start_time + sess_time)
        latest_readable = ts_to_date(int(latest_ts))
        re_write_l_s(self.total_this_week, total_forever, latest_ts, latest_readable)

    def close(self):
        self.active = False
        self.total_this_week = self.get_total_this_week()
        self.write_l_s()

    def summary(self):
        print 'Session summary'
        print 'Total time accum: %d' % self.total_this_week

#
# call the session
#
sess = Session(get_current_time())

#
# run the loooop!!
#

def update_l_s(update_stop):
    # update files here
    # re_write_l_s(sess.get_total_this_week())
    if not update_stop.is_set():
        # call update_l_s every 60
        threading.Timer(2, update_l_s, [update_stop]).start()

update_stop = threading.Event()
update_l_s(update_stop)

while sess.active:
    input = raw_input('eo > ')
    if (input == 'close'):
        update_stop.set()
        sess.close()
    elif (input == 'session'):
        print sess.get_total_session_time()
#
# clean up the session
#
sess.summary()
