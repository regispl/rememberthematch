import unittest

from rememberthematch.match import Match
from rememberthematch.filter import TeamNameFilter


class TeamNameFilterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_matches(self):
        m1 = Match(1, "teamA", "teamB", "venue1")
        m2 = Match(2, "teamB", "teamC", "venue2")
        m3 = Match(2, "teamC", "teamA", "venue3")
        matches = [m1, m2, m3]

        return matches

    def test_filter_matches(self):
        name = "teamA"
        filter = TeamNameFilter([name])
        matches = self.get_matches()
        matches = filter.filter(matches)

        self.assertEquals(2, len(matches))
        self.assertEquals(name, matches[0].home_team)
        self.assertEquals(name, matches[1].away_team)

    def test_filter_no_matches(self):
        name = "teamX"
        filter = TeamNameFilter([name])
        matches = self.get_matches()
        matches = filter.filter(matches)

        self.assertEquals(0, len(matches))
