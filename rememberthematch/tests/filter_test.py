import time
import unittest

from datetime import datetime

from rememberthematch.match import Match
from rememberthematch.filter import TeamNameFilter, DateFilter


class TeamNameFilterTest(unittest.TestCase):

    def get_matches(self):
        m1 = Match(1, "teamA", "teamB", "venue1")
        m2 = Match(2, "teamB", "teamC", "venue2")
        m3 = Match(2, "teamC", "teamA", "venue3")
        matches = [m1, m2, m3]

        return matches

    def test_filter_matches(self):
        f = TeamNameFilter(["teamA"])
        matches = self.get_matches()
        matches_f = f.filter(matches)

        self.assertEquals(2, len(matches_f))
        self.assertEquals(matches[0], matches_f[0])
        self.assertEquals(matches[2], matches_f[1])

    def test_filter_no_matches(self):
        f = TeamNameFilter(["teamX"])
        matches = self.get_matches()
        matches_f = f.filter(matches)

        self.assertEquals(0, len(matches_f))

    def test_filter_matches_only_given_teams(self):
        f = TeamNameFilter(["teamA", "teamC"], only_these_teams=True)
        matches = self.get_matches()
        matches_f = f.filter(matches)

        self.assertEquals(1, len(matches_f))
        self.assertEquals(matches[2], matches_f[0])

    def test_filter_no_matches_only_given_teams(self):
        f = TeamNameFilter(["teamX", "teamY"], only_these_teams=True)
        matches = self.get_matches()
        matches_f = f.filter(matches)

        self.assertEquals(0, len(matches_f))


class DateFilterTest(unittest.TestCase):

    def get_timestamp(self, date):
        return time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple())

    def get_matches(self):
        m1 = Match(self.get_timestamp("2014-07-26"), "teamA", "teamB", "venue1")
        m2 = Match(self.get_timestamp("2014-08-16"), "teamB", "teamC", "venue2")
        m3 = Match(self.get_timestamp("2014-11-11"), "teamC", "teamA", "venue3")
        m4 = Match(self.get_timestamp("2015-01-26"), "teamD", "teamC", "venue4")
        m5 = Match(self.get_timestamp("2015-05-04"), "teamA", "teamD", "venue1")
        matches = [m1, m2, m3, m4, m5]

        return matches

    def test_filter_min_date_only(self):
        min_date = "2014-11-11"
        f = DateFilter(min=min_date)
        matches = self.get_matches()
        matches_f = f.filter(matches)

        self.assertEquals(3, len(matches_f))
        self.assertEqual(matches[2], matches_f[0])
        self.assertEqual(matches[3], matches_f[1])
        self.assertEqual(matches[4], matches_f[2])

    def test_filter_max_date_only(self):
        max_date = "2014-11-11"
        f = DateFilter(max=max_date)
        matches = self.get_matches()
        matches_f = f.filter(matches)

        self.assertEquals(3, len(matches_f))
        self.assertEqual(matches[0], matches_f[0])
        self.assertEqual(matches[1], matches_f[1])
        self.assertEqual(matches[2], matches_f[2])

    def test_filter_min_and_max_date(self):
        min_date = "2014-08-16"
        max_date = "2015-01-26"
        f = DateFilter(min=min_date, max=max_date)
        matches = self.get_matches()
        matches_f = f.filter(matches)

        self.assertEquals(3, len(matches_f))
        self.assertEqual(matches[1], matches_f[0])
        self.assertEqual(matches[2], matches_f[1])
        self.assertEqual(matches[3], matches_f[2])

    def test_filter_no_dates(self):
        f = DateFilter()
        matches = self.get_matches()
        matches_f = f.filter(matches)

        self.assertEquals(5, len(matches_f))
        self.assertEqual(matches[0], matches_f[0])
        self.assertEqual(matches[1], matches_f[1])
        self.assertEqual(matches[2], matches_f[2])
        self.assertEqual(matches[3], matches_f[3])
        self.assertEqual(matches[4], matches_f[4])