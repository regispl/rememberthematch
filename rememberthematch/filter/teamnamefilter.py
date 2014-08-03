from abstract import AbstractFilter


class TeamNameFilter(AbstractFilter):

    def __init__(self, names, only_these_teams=False):
        super(TeamNameFilter, self).__init__()
        self.names = names
        self.only_these_teams = only_these_teams

    def filter_item(self, item):
        if self.only_these_teams:
            return item.home_team in self.names and item.away_team in self.names
        else:
            return item.home_team in self.names or item.away_team in self.names
