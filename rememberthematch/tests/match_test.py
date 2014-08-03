import unittest
from rememberthematch.match import Match


class MatchTest(unittest.TestCase):

    def test_matches_are_equal(self):
        m1 = Match(1, "teamA", "teamB", "venue")
        m2 = Match(1, "teamA", "teamB", "venue")

        self.assertEqual(m1, m2)

    def test_matches_are_equal_case_insensitive(self):
        m1 = Match(1, "teamA", "teamB", "venue")
        m2 = Match(1, "TeamA", "TeamB", "venue")

        self.assertEqual(m1, m2)

    def test_matches_are_not_equal(self):
        m = Match(1, "teamA", "teamB", "venue")
        m1 = Match(2, "teamA", "teamB", "venue")
        m2 = Match(1, "teamX", "teamB", "venue")
        m3 = Match(1, "teamA", "teamX", "venue")
        m4 = Match(1, "teamA", "teamB", "venueX")

        self.assertNotEqual(m, m1)
        self.assertNotEqual(m, m2)
        self.assertNotEqual(m, m3)
        self.assertNotEqual(m, m4)

    def test_match_get_date(self):
        m = Match(1, "teamA", "teamB", "venue")

        self.assertEqual(m.date, "1970-01-01")