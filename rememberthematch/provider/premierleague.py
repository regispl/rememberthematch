from rememberthematch.provider.abstract import AbstractDataProvider

from calendar import timegm
from datetime import datetime


class PremierLeagueDataProvider(AbstractDataProvider):

    DATETIME_PARSER_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def date_to_timestamp(self, datetime_string):
        timestamp = int(timegm(datetime.strptime(datetime_string[:-5], self.DATETIME_PARSER_FORMAT).timetuple()))
        timestamp -= 7200  # FIXME: Timezone hack - %z (timezone offset) not supported, so I hardcoded the conversion to GMT
        return timestamp

    def get(self):
        try:
            matches = self.client.get_all_matches()

            parsed = []
            for match in matches:
                match['timestamp'] = self.date_to_timestamp(match['timestamp'])
                parsed.append(match)

            return parsed
        except Exception, e:
            raise Exception("Failed to parse input data: %s" % e)
