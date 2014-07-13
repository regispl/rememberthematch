import logging
import urllib2


class UrlDownloaderException(Exception):
    pass


class UrlDownloader(object):
    DEFAULT_USERAGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153"

    def __init__(self, user_agent=None):
        self.logger = logging.getLogger(__name__)
        self.user_agent = user_agent if user_agent else self.DEFAULT_USERAGENT

    def download(self, baseurl, params):
        url = baseurl % params
        headers = {'User-agent': self.user_agent}
        request = urllib2.Request(url, headers=headers)

        try:
            self.logger.info("Accessing URL: %s" % url)
            response = urllib2.urlopen(request)
            html = response.read()
            self.logger.info("Received response. Content length: %s" % len(html))
        except Exception, e:
            raise UrlDownloaderException("Failed to download website's contents!")

        return html