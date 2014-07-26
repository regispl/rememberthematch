from abstract import AbstractFilter


class TeamNameFilter(AbstractFilter):

    def __init__(self, names):
        super(TeamNameFilter, self).__init__()
        self.names = names

    def filter_item(self, item):
        return item.home_team in self.names or item.away_team in self.names
