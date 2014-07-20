import logging
import urllib

from bs4 import BeautifulSoup
from calendar import timegm
from datetime import datetime

from urldownloader import UrlDownloader


class PremierLeagueHTMLParser(object):

    # http://www.premierleague.com/ajax/site-header/ajax-all-fixtures.json
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

    def __init__(self, downloader=None):
        self.logger = logging.getLogger(__name__)
        self.downloader = downloader if downloader else UrlDownloader()

    def get_formatted_date(self, header):
        date_part = header.text.strip().split(" ")
        if len(date_part[1]) == 1:
            date_part[1] = "0" + date_part[1]
        return " ".join(date_part)

    def get_date_timestamp(self, date, time):
        datetime_string = "%s %s" % (date, time)
        return int(timegm(datetime.strptime(datetime_string, self.DATETIME_PARSER_FORMAT).timetuple()))

    def parse_html(self, html):
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
        html = self.downloader.download(url)

        try:
            return self.parse_html(html)
        except Exception, e:
            raise Exception("Failed to parse HTML: %s" % e.message)