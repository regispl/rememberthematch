import os
import unittest
from mockito import *
from mockito import any as mock_any
from rememberthematch.parser import PremierLeagueHTMLParser
from rememberthematch.urldownloader import UrlDownloader


class PremierLeagueHTMLParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        unstub()

    def get_path(self, filename):
        dir = os.path.dirname(__file__)
        return os.path.join(dir, filename)

    def testParseSampleHtmlSuccessfully(self):
        with open(self.get_path("data/premierleague.html")) as f:
            static_html = f.read()
            downloader = mock(UrlDownloader)
            when(downloader).download(mock_any()).thenReturn(static_html)
            parser = PremierLeagueHTMLParser(downloader)
            output = parser.parse()
            timestamps = [int(match['timestamp']) for match in output]
            self.assertEqual(1432479600, max(timestamps))
            self.assertEqual(1408201200, min(timestamps))
            self.assertEqual(380, len(output))