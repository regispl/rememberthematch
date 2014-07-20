import logging
from abc import abstractmethod
from rememberthematch.urldownloader import UrlDownloader


class AbstractParser(object):

    def __init__(self, downloader=None):
        self.logger = logging.getLogger(__name__)
        self.downloader = downloader if downloader else UrlDownloader()

    @abstractmethod
    def parse(self):
        pass