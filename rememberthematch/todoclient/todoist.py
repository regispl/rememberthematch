import logging
from datetime import datetime
from pytodoist import todoist
from abstract import AbstractToDoClient


class TodoistClient(AbstractToDoClient):

    DATE_FORMAT = "%d.%m.%Y %H:%M"
    DEFAULT_PRIORITY = 3

    def __init__(self, username, password, project, dry_run=True):
        super(TodoistClient, self).__init__(dry_run)
        self.logger = logging.getLogger(__name__)
        self.project = project

        try:
            self.user = todoist.login(username, password)
        except Exception, e:
            raise Exception("Failed to log in to Todoist as user %s. Reason: %s" % (username, e))

        self.logger.info("Logged in to Todoist as %s" % username)

        if self.dry_run:
            self.logger.info("Running in dry-run mode!")

    def add_task(self, name, timestamp, priority=None):
        priority = priority if priority else self.DEFAULT_PRIORITY
        date = datetime.fromtimestamp(timestamp).strftime(self.DATE_FORMAT)

        log_message = "(dry-run) " if self.dry_run else ""
        log_message += "Adding task: %s %s %s" % (date, name, priority)
        self.logger.info(log_message)

        if not self.dry_run:
            self.user.get_project(self.project).add_task(name, date=date, priority=priority)
