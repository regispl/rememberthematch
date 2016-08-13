import grequests


# TODO: Add AbstractClient
# FIXME: This guy is more than a client ATM, should not process the data - it's temporary (at least it should be ;-) )
class PremierLeagueAPIClient:

    BASE_URL = "https://sportsop-soccer-sports-open-data-v1.p.mashape.com"
    VERSION = "v1"

    HEADERS = {
        "X-Mashape-Key": None,
        "Accept": "application/json"
    }

    LEAGUE_SLUG = "premier-league"
    SEASON_SLUG = "16-17"

    def __init__(self, api_key):
        self.HEADERS.update({
            "X-Mashape-Key": api_key
        })

    def get_all_rounds(self):
        url = "%(base_url)s/%(version)s/leagues/%(league_slug)s/seasons/%(season_slug)s"
        params = {
            "base_url": self.BASE_URL,
            "version": self.VERSION,
            "league_slug": self.LEAGUE_SLUG,
            "season_slug": self.SEASON_SLUG
        }

        rs = [grequests.get(url % params, headers=self.HEADERS)]
        rounds_json = grequests.map(rs)[0].json()['data']['rounds']

        rounds = []
        for round in rounds_json:
            rounds.append(round['round_slug'])

        return rounds

    def get_all_matches(self):
        url = "%(base_url)s/%(version)s/leagues/%(league_slug)s/seasons/%(season_slug)s/rounds/%(round_slug)s/matches"
        params_base = {
            "base_url": self.BASE_URL,
            "version": self.VERSION,
            "league_slug": self.LEAGUE_SLUG,
            "season_slug": self.SEASON_SLUG
        }

        rounds = self.get_all_rounds()

        rs = []
        for round in rounds:
            params = params_base.copy()
            params.update({
                "round_slug": round
            })
            rs.append(grequests.get(url % params, headers=self.HEADERS))

        resp = grequests.map(rs)

        matches_all = []
        for r in resp:
            matches = r.json()['data']['matches']
            for match in matches:
                match_data = {
                    'homeTeamName': match['home']['team'],
                    'awayTeamName': match['away']['team'],
                    'timestamp': match['date_match'],
                    'venue': '<unknown>'
                }
                matches_all.append(match_data)

        return matches_all
