import logging
import todoist
from datetime import datetime
from abstract import AbstractToDoClient


class TodoistClient(AbstractToDoClient):

    DATE_FORMAT = "%d/%m/%Y at %H:%M"
    DEFAULT_PRIORITY = 3

    def __init__(self, api_token, project, dry_run=False):
        super(TodoistClient, self).__init__(dry_run)
        self.logger = logging.getLogger(__name__)
        self.api = todoist.TodoistAPI(api_token)

        self.logger.info("Logged in to Todoist as %s" % self.api.user)
        self.logger.info("Using default priority %s unless different value is provided" % self.DEFAULT_PRIORITY)

        self.api.sync()
        self.api.projects.sync()
        self.api.items.sync()

        self.project_id = self.get_project_id_by_name(project)

        if self.dry_run:
            self.logger.info("Running in dry-run mode!")

    def get_project_id_by_name(self, project):
        projects = self.api.projects.all(lambda p: p['name'] == project)
        if not projects or len(projects) == 0:
            raise Exception("Could not find project %s" % project)
        elif len(projects) > 1:
            raise Exception("Found more than one project matching name %s" % project)
        else:
            return projects[0]['id']

    def add_task(self, name, timestamp, priority=None):
        priority = priority if priority else self.DEFAULT_PRIORITY
        date = datetime.fromtimestamp(timestamp).strftime(self.DATE_FORMAT)

        log_message = "(dry-run) " if self.dry_run else ""
        log_message += "Adding task: %s %s" % (date, name)
        self.logger.info(log_message)

        if not self.dry_run:
            self.api.items.add(name, self.project_id, date_string=date, priority=priority)

    def commit(self):
        self.api.commit()
