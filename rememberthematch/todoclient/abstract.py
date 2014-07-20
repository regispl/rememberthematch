from abc import ABCMeta, abstractmethod


class AbstractToDoClient(object):
    __metaclass__ = ABCMeta

    def __init__(self, dry_run=True):
        self.dry_run = dry_run

    @abstractmethod
    def add_task(self, timestamp, name, priority=None):
        pass
