import logging

from rememberthematch.parser.premierleague import PremierLeagueJSONParser
from todoclient import TodoistClient


class RememberTheMatch(object):

    TASK_NAME_FORMAT = "%s vs. %s at %s"

    def __init__(self, username, password, project, interactive=True, dry_run=True):
        self.logger = logging.getLogger(__name__)
        self.parser = PremierLeagueJSONParser()
        self.username = username
        self.password = password
        self.project = project
        self.interactive = interactive
        self.dry_run = dry_run

        # TODO: needs to be dynamic pasing on script arguments
        self.client = TodoistClient(self.username, self.password, self.project)

    def print_schedule(self, matches):
        for match in matches:
            self.logger.info("%(timestamp)s: %(homeTeamName)s vs. %(awayTeamName)s at %(venue)s" % match)

    def add_tasks(self, matches):
        for match in matches:
            timestamp = match['timestamp']
            home_team = match['homeTeamName']
            away_team = match['awayTeamName']
            venue = match['venue']['name']

            task_name = self.TASK_NAME_FORMAT % (home_team, away_team, venue)
            self.client.add_task(timestamp, task_name)

    def run(self):
        matches = self.parser.parse()
        self.add_tasks(matches)