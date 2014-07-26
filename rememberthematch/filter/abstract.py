import logging
from abc import abstractmethod


class AbstractFilter(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        pass

    """
    Return True if item should be kept in collection.
    Return False to remove item.
    """
    @abstractmethod
    def filter_item(self, item):
        pass

    def filter(self, data):
        filtered_data = [d for d in data if self.filter_item(d)]
        self.logger.info("Filtered out %d of %d matches" % (len(filtered_data), len(data)))
        return filtered_data
