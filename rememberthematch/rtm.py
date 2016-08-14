import logging

from match import Match
from provider.premierleague import PremierLeagueDataProvider
from todoclient import TodoistClient

from rememberthematch.client.ssod import PremierLeagueAPIClient


class RememberTheMatch(object):

    # FIXME: Add back the location - need to be retrieved from Sports Open Data API
    #TASK_NAME_FORMAT = "%s vs. %s at %s"
    TASK_NAME_FORMAT = "%s vs. %s"

    def __init__(self, api_key, todoclient_config, filters, interactive=True):
        self.logger = logging.getLogger(__name__)
        logging.getLogger("requests").setLevel(logging.WARNING)

        self.parser = PremierLeagueDataProvider(client=PremierLeagueAPIClient(api_key))

        self.filters = filters

        # TodoClient Configuration
        self.api_token = todoclient_config.api_token
        self.project = todoclient_config.project
        self.dry_run = todoclient_config.dry_run

        self.interactive = interactive

        # TODO: needs to be dynamic based on script arguments
        self.client = TodoistClient(self.api_token, self.project, dry_run=self.dry_run)

    def print_schedule(self, matches):
        for match in matches:
            self.logger.info("%(timestamp)s: %(homeTeamName)s vs. %(awayTeamName)s at %(venue)s" % match)

    def get_matches(self, data):
        matches = []
        for item in data:
            timestamp = item['timestamp']
            home_team = item['homeTeamName']
            away_team = item['awayTeamName']
            venue = item['venue']
            matches.append(Match(timestamp, home_team, away_team, venue))
        return matches

    def add_tasks(self, matches):
        for match in matches:
            task = self.TASK_NAME_FORMAT % (match.home_team, match.away_team)
            self.client.add_task(task, match.timestamp)
        if len(matches) > 0:
            self.client.commit()

    def run(self):
        matches = self.get_matches(self.parser.get())

        for filter in self.filters:
            matches = filter.filter(matches)

        self.add_tasks(matches)