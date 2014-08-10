import logging
import webbrowser

from rtmapi import Rtm
from abstract import AbstractToDoClient


class RememberTheMilkClient(AbstractToDoClient):

    PERMS = "write"

    def __init__(self, api_key, shared_secret, list_name, dry_run=False):
        super(RememberTheMilkClient, self).__init__(dry_run)
        self.logger = logging.getLogger(__name__)
        self.token = None

        self.api = Rtm(api_key, shared_secret, self.PERMS)
        self.maybe_get_token()
        self.timeline = self.get_timeline()
        self.set_default_list(list_name)

        if self.dry_run:
            self.logger.info("Running in dry-run mode!")

    def maybe_get_token(self):
        if not self.api.token_valid():
            url, frob = self.api.authenticate_desktop()
            webbrowser.open(url)
            raw_input("Press Enter if you already authorized Remember The Match app " +
                      "to use your Remember The Milk account...")
            self.api.retrieve_token(frob)
            self.token = self.api.token

    def get_timeline(self):
        result = self.api.rtm.timelines.create()
        return result.timeline.value

    def set_default_list(self, name):
        result = self.api.rtm.lists.getList()
        print result
        print result.lists
        print result.lists.list
        for list in result.lists.list:
            print "LIST:", list
            if list.name == name:
                self.api.rtm.lists.setDefaultList(timeline=list.timeline, list_id=list.id)
                return
        raise Exception("List %s was not found" % name)

    def add_task(self, name, timestamp, priority=None):
        date = timestamp

        log_message = "(dry-run) " if self.dry_run else ""
        log_message += "Adding task: %s %s %s" % (date, name, priority)
        self.logger.info(log_message)

        if not self.dry_run:
            self.api.rtm.tasks.add(timeline=self.timeline,
                                   list_id=self.list_id,
                                   name=name)
