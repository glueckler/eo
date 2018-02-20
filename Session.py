from helpers import *

class Session:
    def __init__(self, current_time):
        self.active = True

        self.start_time = current_time

        self.current_week = ts_to_week(self.start_time)

        self.total_this_week = int(l_s_read_line(0))
        self.total_forever = int(l_s_read_line(1))
        latest_week_ts = int(l_s_read_line(2))
        self.latest_week = ts_to_week(latest_week_ts)

        is_same_week = self.latest_week == self.current_week
        if (not is_same_week):
            self.total_this_week = 0

        current_month = get_month()
        self.total_this_month = total_for_month(current_month)
        if self.total_this_month:
            self.total_this_month = int(self.total_this_month)
        else:
            self.total_this_month = 0


    def get_total_session_time(self):
        return get_time_passed(self.start_time, get_current_time())

    def get_total_this_week(self):
        return self.get_total_session_time() + self.total_this_week

    def close(self):
        self.active = False
        self.total_this_week = self.get_total_this_week()
        self.write_l_s()

        self.total_this_month = self.total_this_month + self.get_total_session_time()
        write_monthly(self.total_this_month)

    def write_l_s(self):
        sess_time = self.get_total_session_time()
        total_forever = str(self.total_forever + sess_time)
        latest_ts = str(self.start_time + sess_time)
        latest_human_readable = ts_to_date(int(latest_ts))
        re_write_l_s(self.total_this_week, total_forever, latest_ts, latest_human_readable)

        
