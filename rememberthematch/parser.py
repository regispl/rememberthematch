import logging
import urllib

from bs4 import BeautifulSoup
from calendar import timegm
from collections import OrderedDict
from datetime import datetime

from urldownloader import UrlDownloader


class PremierLeagueHTMLParser(object):

    # http://www.premierleague.com/ajax/site-header/ajax-all-fixtures.json
    baseurl = "http://www.premierleague.com/en-gb/matchday/matches.html?%s"
    params = urllib.urlencode({
        "paramClubId": "ALL",
        "paramComp_100": "true",
        "view": ".dateSeason"
    })

    def __init__(self, downloader=None):
        self.logger = logging.getLogger(__name__)
        self.downloader = downloader if downloader else UrlDownloader()

    def get_date_timestamp(self, header):
        date_part = header.text.strip().split(" ")
        if len(date_part[1]) == 1:
            date_part[1] = "0" + date_part[1]
        date_string = " ".join(date_part)
        date_timestamp = int(timegm(datetime.strptime(date_string, "%A %d %B %Y").timetuple()))
        return date_timestamp

    def parse_html(self, html):
        data = OrderedDict()
        soup = BeautifulSoup(html)
        contents = soup.body.find('div', attrs={'widget': 'fixturelistbroadcasters'})
        rows = contents.find_all('tr')
        date_timestamp = None
        for row in rows:
            header = row.find('th')
            if header:
                date_timestamp = self.get_date_timestamp(header)
                data[date_timestamp] = []
                continue

            cells = row.find_all('td')
            values = []
            for cell in cells:
                values.append(cell.get_text(strip=True))
            match = {
                'time': values[1],
                'teams': values[2],
                'stadium': values[3]
            }
            data[date_timestamp].append(match)
        return data

    def parse(self):
        url = self.baseurl % self.params
        html = self.downloader.download(url)
        return self.parse_html(html)
