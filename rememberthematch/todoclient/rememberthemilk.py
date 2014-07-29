import logging
import webbrowser

from rtmapi import Rtm
from abstract import AbstractToDoClient


class RememberTheMilkClient(AbstractToDoClient):

    def __init__(self, api_key, shared_secret, project, dry_run=False):
        super(RememberTheMilkClient, self).__init__(dry_run)
        self.logger = logging.getLogger(__name__)
        self.project = project
        self.token = None

        self.api = Rtm(api_key, shared_secret, "delete")
        self.get_token()
        self.timeline = self.get_timeline()
        self.list_id = self.get_list()

        if self.dry_run:
            self.logger.info("Running in dry-run mode!")

    def get_token(self):
        url, frob = self.api.authenticate_desktop()
        webbrowser.open(url)
        self.api.retrieve_token(frob)
        self.token = self.api.token

    def get_timeline(self):
        result = self.api.rtm.timelines.create()
        return result.timeline.value

    def get_list(self):
        return 1

    def add_task(self, name, timestamp, priority=None):
        date = timestamp

        log_message = "(dry-run) " if self.dry_run else ""
        log_message += "Adding task: %s %s %s" % (date, name, priority)
        self.logger.info(log_message)

        if not self.dry_run:
            self.api.rtm.tasks.add(timeline=self.timeline,
                                   list_id=self.list_id,
                                   name=name)
