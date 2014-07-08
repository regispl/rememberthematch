import logging
from abstract import AbstractToDoClient
from pytodoist import todoist

class TodoistClient(AbstractToDoClient):

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

    def add_task(self, date, time, name):
        self.logger.info("Adding task: %s %s %s" % (date, time, name))
        #self.user.get_project(self.project).add_task(name)
        pass