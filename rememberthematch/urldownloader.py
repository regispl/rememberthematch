import logging
import urllib2


class UrlDownloader(object):

    def __init__(self, user_agent):
        self.logger = logging.getLogger(__name__)
        self.user_agent = user_agent

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
            print "Failed to download website's contents:", e

        return html