import logging

from rememberthematch.parser.premierleague import PremierLeagueJSONParser
from todoclient import TodoistClient


class RememberTheMatch(object):

    TASK_NAME_FORMAT = "%s vs. %s at %s"

    def __init__(self, todoclient_config, interactive=True):
        self.logger = logging.getLogger(__name__)
        self.parser = PremierLeagueJSONParser()

        # TodoClient Configuration
        self.username = todoclient_config.username
        self.password = todoclient_config.password
        self.project = todoclient_config.project
        self.dry_run = todoclient_config.dry_run

        self.interactive = interactive

        # TODO: needs to be dynamic basing on script arguments
        self.client = TodoistClient(self.username, self.password, self.project, dry_run=self.dry_run)

    def print_schedule(self, matches):
        for match in matches:
            self.logger.info("%(timestamp)s: %(homeTeamName)s vs. %(awayTeamName)s at %(venue)s" % match)

    def add_tasks(self, matches):
        for match in matches:
            timestamp = match['timestamp']
            home_team = match['homeTeamName']
            away_team = match['awayTeamName']
            venue = match['venue']['name']

            task = self.TASK_NAME_FORMAT % (home_team, away_team, venue)
            self.client.add_task(task, timestamp)

    def run(self):
        matches = self.parser.parse()
        self.add_tasks(matches)