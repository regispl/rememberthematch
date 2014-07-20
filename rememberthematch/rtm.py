import logging

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

    def print_schedule(self, matches):
        for match in matches:
            self.logger.info("%(timestamp)s: %(homeTeamName)s vs. %(awayTeamName)s at %(venue)s" % match)

    def run(self):
        matches = self.parser.parse()
        self.print_schedule(matches)

        # TODO: needs to be dynamic pasing on script arguments
        todoist_client = TodoistClient(self.username, self.password, self.project)

        for match in matches:
            timestamp = match['timestamp']
            home_team = match['homeTeamName']
            away_team = match['awayTeamName']
            venue = match['venue']['name']

            task_name = "%s vs. %s at %s" % (home_team, away_team, venue)
            todoist_client.add_task(timestamp, task_name, venue)