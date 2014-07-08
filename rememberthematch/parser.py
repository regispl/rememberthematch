import logging
import urllib
import urllib2
from bs4 import BeautifulSoup
from calendar import timegm
from datetime import datetime
from collections import OrderedDict


class UrlDownloader(object):

    def __init__(self, user_agent):
        self.logger = logging.getLogger(__name__)
        self.user_agent = user_agent

    def download(self, baseurl, params):
        url = baseurl % params
        headers = {'User-agent': self.user_agent}
        request = urllib2.Request(url, headers=headers)

        try:
            self.logger.info("Accessing URL: %s" % url)
            response = urllib2.urlopen(request)
            html = response.read()
            self.logger.info("Received response. Content length: %s" % len(html))
        except Exception, e:
            print "Failed to download website's contents:", e

        return html


class PremierLeagueParser(object):

    # http://www.premierleague.com/ajax/site-header/ajax-all-fixtures.json
    baseurl = "http://www.premierleague.com/en-gb/matchday/matches.html?%s"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153"
    params = urllib.urlencode({
        "paramClubId": "ALL",
        "paramComp_100": "true",
        "view": ".dateSeason"
    })

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.downloader = UrlDownloader(self.user_agent)

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
        html = self.downloader.download(self.baseurl, self.params)
        return self.parse_html(html)
