from abc import ABCMeta, abstractmethod


class AbstractToDoClient(object):
    __metaclass__ = ABCMeta

    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    @abstractmethod
    def add_task(self, name, timestamp, priority=None):
        pass

    @abstractmethod
    def commit(self):
        pass
