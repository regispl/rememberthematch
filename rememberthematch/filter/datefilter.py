import sys
import time
from datetime import datetime
from abstract import AbstractFilter


class DateFilter(AbstractFilter):

    MIN_TIMESTAMP = 0
    MAX_TIMESTAMP = sys.maxint

    def __init__(self, min=None, max=None):
        super(DateFilter, self).__init__()
        self.min = self.to_timestamp(min) if min else self.MIN_TIMESTAMP
        self.max = self.to_timestamp(max) if max else self.MAX_TIMESTAMP

    def to_timestamp(self, date):
        return time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple())

    def filter_item(self, item):
        return self.min <= item.timestamp <= self.max
