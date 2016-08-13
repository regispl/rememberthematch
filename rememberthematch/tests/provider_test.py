import os
import unittest

from mockito import *
from mockito import any as mock_any

from rememberthematch.provider.premierleague import PremierLeagueDataProvider
from rememberthematch.client.ssod import PremierLeagueAPIClient


class BaseParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        unstub()


class PremierLeagueDataProviderTest(BaseParserTest):

    def test_parse_and_return_correct_data(self):
        client = mock(PremierLeagueAPIClient)
        when(client).get_all_matches().thenReturn([
            {'homeTeamName': 'TeamA', 'awayTeamName': 'TeamF', 'timestamp': '2016-08-14T17:50:14+0200', 'venue': '<unknown>'},
            {'homeTeamName': 'TeamB', 'awayTeamName': 'TeamE', 'timestamp': '2016-02-01T17:00:00+0200', 'venue': '<unknown>'},
            {'homeTeamName': 'TeamC', 'awayTeamName': 'TeamD', 'timestamp': '2016-12-25T14:30:00+0200', 'venue': '<unknown>'}
        ])

        parser = PremierLeagueDataProvider(client=client)
        output = parser.get()

        self.assertEqual(output[0]['timestamp'], 1471189814)
        self.assertEqual(output[1]['timestamp'], 1454338800)
        self.assertEqual(output[2]['timestamp'], 1482669000)
