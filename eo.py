#!/usr/bin/env python
print 'empty objects'

from helpers import *
from Session import Session

# check if temp file exists and recreate the last session file if it does
l_s_clean()

# call the session
print 'initializing Session :)'
sess = Session(get_current_time())

# print initial session info
print 'current week: week %d' % sess.current_week
print 'total time accumalated.. %s' % secs_to_hours(sess.total_this_week)

# set up the timer stop and call timer
update_stop = threading.Event()
update_l_s(update_stop)

# run the loooop!!
while sess.active:
    raw_in = raw_input('eo > ')
    if (raw_in == 'close'):
        update_stop.set()
        sess.close()
    elif (raw_in == 'session'):
        print sess.get_total_session_time()

# print info on the session
print 'Session summary'
print 'Total time accum: %s' % secs_to_hours(sess.total_this_week)
