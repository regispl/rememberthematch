from abstract import AbstractFilter


class TeamNameFilter(AbstractFilter):

    def __init__(self, names, only_these_teams=False):
        super(TeamNameFilter, self).__init__()
        self.names = [name.lower() for name in names]
        self.only_these_teams = only_these_teams

    def filter_item(self, item):
        home_team = item.home_team.lower()
        away_team = item.away_team.lower()
        if self.only_these_teams:
            return home_team in self.names and away_team in self.names
        else:
            return home_team in self.names or away_team in self.names
