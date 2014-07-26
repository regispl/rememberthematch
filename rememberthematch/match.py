from datetime import datetime


class Match(object):

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, timestamp, home_team, away_team, venue):
        self.timestamp = timestamp
        self.home_team = home_team
        self.away_team = away_team
        self.venue = venue

    @property
    def date(self):
        return datetime.fromtimestamp(self.timestamp).strftime(self.DATE_FORMAT)

    def __eq__(self, other):
        return self.timestamp == other.timestamp and \
            self.home_team == other.home_team and \
            self.away_team == other.away_team and \
            self.venue == other.venue

    def __str__(self):
        return "Match(timestamp=%d [%s], home_team=%s, away_team=%s, venue=%s)" % \
            (self.timestamp, self.date, self.home_team, self.away_team, self.venue)
