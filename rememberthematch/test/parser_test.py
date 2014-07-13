import os
import unittest
from mockito import *
from rememberthematch.parser import PremierLeagueHTMLParser
from rememberthematch.urldownloader import UrlDownloader


class PremierLeagueHTMLParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = PremierLeagueHTMLParser()

    def tearDown(self):
        unstub()

    def get_path(self, filename):
        dir = os.path.dirname(__file__)
        return os.path.join(dir, filename)

    def testParseSampleHtmlSuccessfully(self):
        downloader = mock(UrlDownloader)
        with open(self.get_path("data/premierleague.html")) as f:
            static_html = f.read()
            when(downloader).download().thenReturn(static_html)
            output = self.parser.parse()
            timestamps = [int(ts) for ts in output.keys()]
            self.assertEqual(1432425600, max(timestamps))
            self.assertEqual(1408147200, min(timestamps))
            self.assertEqual(41, len(output))