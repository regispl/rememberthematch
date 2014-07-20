import json
import urllib

from bs4 import BeautifulSoup
from calendar import timegm
from datetime import datetime

from rememberthematch.parser.abstract import AbstractParser


class PremierLeagueJSONParser(AbstractParser):

    URL = "http://www.premierleague.com/ajax/site-header/ajax-all-fixtures.json"

    def parse_input(self, json_input):
        json_parsed = json.loads(json_input)
        matches = json_parsed['siteHeaderSection']['matches']

        # Dummy conversion from millis to seconds
        for match in matches:
            match['timestamp'] /= 1000

        return matches

    def parse(self):
        input_data = self.downloader.download(self.URL)

        try:
            return self.parse_input(input_data)
        except Exception, e:
            raise Exception("Failed to parse input data: %s" % e.message)


class PremierLeagueHTMLParser(AbstractParser):

    BASE_URL = "http://www.premierleague.com/en-gb/matchday/matches.html?%s"
    PARAMS = urllib.urlencode({
        "paramClubId": "ALL",
        "paramComp_100": "true",
        "view": ".dateSeason"
    })

    DATETIME_PARSER_FORMAT = "%A %d %B %Y %H:%M"
    TEAM_SEPARATOR = " v "

    DATA_TIME_IDX = 1
    DATA_TEAMS_IDX = 2
    DATA_VENUE_IDX = 3

    def get_formatted_date(self, header):
        date_part = header.text.strip().split(" ")
        if len(date_part[1]) == 1:
            date_part[1] = "0" + date_part[1]
        return " ".join(date_part)

    def get_date_timestamp(self, date, time):
        datetime_string = "%s %s" % (date, time)
        timestamp = int(timegm(datetime.strptime(datetime_string, self.DATETIME_PARSER_FORMAT).timetuple()))
        timestamp -= 3600  # FIXME: Timezone hack (to GMT)
        return timestamp

    def parse_input(self, html):
        data = []
        soup = BeautifulSoup(html)
        contents = soup.body.find('div', attrs={'widget': 'fixturelistbroadcasters'})
        rows = contents.find_all('tr')
        match_date = None
        for row in rows:

            # If header, get date and skip
            header = row.find('th')
            if header:
                match_date = self.get_formatted_date(header)
                continue

            # TODO: retrieve by td.class?
            cells = row.find_all('td')
            values = []
            for cell in cells:
                values.append(cell.get_text(strip=True))

            # Extra lines with comments on the schedule
            if len(values) != 6:
                continue

            match_time = values[self.DATA_TIME_IDX]
            timestamp = self.get_date_timestamp(match_date, match_time)
            home_team, away_team = values[self.DATA_TEAMS_IDX].split(self.TEAM_SEPARATOR)
            venue = values[self.DATA_VENUE_IDX]

            match = {
                'timestamp': timestamp,
                'homeTeamName': home_team,
                'awayTeamName': away_team,
                'venue': {
                    'name': venue
                }
            }
            data.append(match)
        return data

    def parse(self):
        url = self.BASE_URL % self.PARAMS
        input_data = self.downloader.download(url)

        try:
            return self.parse_input(input_data)
        except Exception, e:
            raise Exception("Failed to parse input data: %s" % e.message)
