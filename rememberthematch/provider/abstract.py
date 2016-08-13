import logging
from abc import abstractmethod

from rememberthematch.client.ssod import PremierLeagueAPIClient


class AbstractDataProvider(object):

    def __init__(self, client):
        self.logger = logging.getLogger(__name__)
        self.client = client

    @abstractmethod
    def get(self):
        pass