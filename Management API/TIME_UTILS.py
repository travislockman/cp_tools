# Time Utility Library
# Used to process datetime, create various date and time stamps
# T. Lockman
# sEpTeMbEr 2020 - cOvId19 h3lL!!!
# O_o tHe pAcKeTs nEvEr LiE o_O #

import datetime
import pytz

class Time_Utils:

    def epoch_utc(self):
        now = datetime.datetime.utcnow()
        now = datetime.datetime.timestamp(now)
        now = str(now).split(".")
        epoch = (int(now[0]) * 1000)
        return epoch

    def iso8601_local(self):
        iso8601 = datetime.datetime.now().isoformat()
        return iso8601

    def iso8601_utc(self):
        iso8601 = datetime.datetime.utcnow().isoformat()
        return iso8601

    def iso8601_converter_from_us(self, datestamp):  # Convert one US datestamp to iso8601
        tz = pytz.timezone('America/New_York')
        dt_object = tz.localize(datetime.datetime.strptime(datestamp, '%Y-%m-%d %H:%M:%S'))
        tz_offset = dt_object.strftime('%z')
        iso8601 = dt_object.strftime(f'%Y-%m-%dT%H:%M:%S{tz_offset}')
        return iso8601
