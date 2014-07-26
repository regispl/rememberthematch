import os
import unittest

from mockito import *
from mockito import any as mock_any

from rememberthematch.parser.premierleague import PremierLeagueJSONParser, PremierLeagueHTMLParser
from rememberthematch.urldownloader import UrlDownloader


class BaseParserTest(unittest.TestCase):

    MAX_TIMESTAMP = 1432476000
    MIN_TIMESTAMP = 1408189500
    NUM_MATCHES = 380

    def setUp(self):
        pass

    def tearDown(self):
        unstub()

    def get_path(self, filename):
        dir = os.path.dirname(__file__)
        return os.path.join(dir, filename)


class PremierLeagueJSONParserTest(BaseParserTest):

    def test_parse_sample_json_successfully(self):
        with open(self.get_path("data/premierleague.json")) as f:
            static_json = f.read()
            downloader = mock(UrlDownloader)
            when(downloader).download(mock_any()).thenReturn(static_json)
            parser = PremierLeagueJSONParser(downloader)
            output = parser.parse()
            timestamps = [int(match['timestamp']) for match in output]
            self.assertEqual(self.MAX_TIMESTAMP, max(timestamps))
            self.assertEqual(self.MIN_TIMESTAMP, min(timestamps))
            self.assertEqual(self.NUM_MATCHES, len(output))


class PremierLeagueHTMLParserTest(BaseParserTest):

    def test_parse_sample_html_successfully(self):
        with open(self.get_path("data/premierleague.html")) as f:
            static_html = f.read()
            downloader = mock(UrlDownloader)
            when(downloader).download(mock_any()).thenReturn(static_html)
            parser = PremierLeagueHTMLParser(downloader)
            output = parser.parse()
            timestamps = [int(match['timestamp']) for match in output]
            self.assertEqual(self.MAX_TIMESTAMP, max(timestamps))
            self.assertEqual(self.MIN_TIMESTAMP, min(timestamps))
            self.assertEqual(self.NUM_MATCHES, len(output))