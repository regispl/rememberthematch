import logging
from datetime import datetime
from pytodoist import todoist
from abstract import AbstractToDoClient


class TodoistClient(AbstractToDoClient):

    DATE_FORMAT = "%d/%m/%Y at %H:%M"
    DEFAULT_PRIORITY = 3

    def __init__(self, username, password, project, dry_run=False):
        super(TodoistClient, self).__init__(dry_run)
        self.logger = logging.getLogger(__name__)

        try:
            self.user = todoist.login(username, password)
        except Exception, e:
            raise Exception("Failed to log in to Todoist as user %s. Reason: %s" % (username, e))

        self.logger.info("Logged in to Todoist as %s" % username)
        self.logger.info("Using default priority %s unless different value is provided" % self.DEFAULT_PRIORITY)

        self.project = self.user.get_project(project)

        if not self.project:
            raise Exception("Could not find project %s" % project)

        if self.dry_run:
            self.logger.info("Running in dry-run mode!")

    def add_task(self, name, timestamp, priority=None):
        priority = priority if priority else self.DEFAULT_PRIORITY
        date = datetime.fromtimestamp(timestamp).strftime(self.DATE_FORMAT)

        log_message = "(dry-run) " if self.dry_run else ""
        log_message += "Adding task: %s %s" % (date, name)
        self.logger.info(log_message)

        if not self.dry_run:
            self.project.add_task(name, date=date, priority=priority)
