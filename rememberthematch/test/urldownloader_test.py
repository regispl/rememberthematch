import unittest
import urllib2
from mockito import *
from StringIO import StringIO
from rememberthematch.urldownloader import UrlDownloader, UrlDownloaderException

MOCK_MESSAGE = "mock message"


def mock_response(req):
    if req.get_full_url() == "http://example.com":
        resp = urllib2.addinfourl(StringIO(MOCK_MESSAGE), "headers", req.get_full_url())
        resp.code = 200
        resp.msg = "OK"
        return resp


class MyHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, req):
        return mock_response(req)


class UrlDownloaderTest(unittest.TestCase):

    def setUp(self):
        my_opener = urllib2.build_opener(MyHTTPHandler)
        urllib2.install_opener(my_opener)
        self.downloader = UrlDownloader()

    def tearDown(self):
        unstub()

    def testDownloaderReturnsExpectedContents(self):
        when(urllib2).urlopen().thenReturn()
        response_message = self.downloader.download("http://example.com")
        verify(urllib2).urlopen()
        self.assertEqual(response_message, MOCK_MESSAGE)

    def testDownloaderRaisesExceptionOnFailure(self):
        when(urllib2).urlopen().thenRaise(Exception("Something went wrong!"))
        with self.assertRaises(UrlDownloaderException):
            self.downloader.download("http://example.com")
