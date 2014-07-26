import logging

from match import Match
from parser.premierleague import PremierLeagueJSONParser
from todoclient import TodoistClient


class RememberTheMatch(object):

    TASK_NAME_FORMAT = "%s vs. %s at %s"

    def __init__(self, todoclient_config, filters, interactive=True):
        self.logger = logging.getLogger(__name__)
        self.parser = PremierLeagueJSONParser()
        self.filters = filters

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

    def get_matches(self, data):
        matches = []
        for item in data:
            timestamp = item['timestamp']
            home_team = item['homeTeamName']
            away_team = item['awayTeamName']
            venue = item['venue']['name']
            matches.append(Match(timestamp, home_team, away_team, venue))
        return matches

    def add_tasks(self, matches):
        for match in matches:
            task = self.TASK_NAME_FORMAT % (match.home_team, match.away_team, match.venue)
            self.client.add_task(task, match.timestamp)

    def run(self):
        matches = self.get_matches(self.parser.parse())

        for filter in self.filters:
            matches = filter.filter(matches)

        self.add_tasks(matches)