import logging

from datetime import datetime

from parser import PremierLeagueHTMLParser
from todoclient import TodoistClient


class RememberTheMatch(object):

    def __init__(self, username, password, project, interactive=True, dry_run=True):
        self.logger = logging.getLogger(__name__)
        self.parser = PremierLeagueHTMLParser()
        self.username = username
        self.password = password
        self.project = project
        self.interactive = interactive
        self.dry_run = dry_run

    def print_schedule(self, data):
        for timestamp, matches in data.items():
            for match in matches:
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                match['date'] = date
                self.logger.info("%(date)s %(time)s: %(teams)s (%(stadium)s)" % match)

    def run(self):
        data = self.parser.parse()
        self.print_schedule(data)
        todoist_client = TodoistClient(self.username, self.password, self.project)

        for timestamp, matches in data.items():
            for match in matches:
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                match['date'] = date
                todoist_client.add_task(match['date'], match['time'], match['teams'])