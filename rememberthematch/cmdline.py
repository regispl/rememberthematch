import argparse
import logging
import sys

from rememberthematch import RememberTheMatch
from rememberthematch.filter import TeamNameFilter, DateFilter
from rememberthematch.todoclient.config import ToDoClientConfiguration


def get_parser():
    parser = argparse.ArgumentParser(description='Never forget about the match you want to watch again!')

    parser.add_argument('--username', '-u', dest='username', action='store', required=True, help='Todoist username')
    parser.add_argument('--password', '-p', dest='password', action='store', required=True, help='Todoist password')
    parser.add_argument('--project', '-pr', dest='project', action='store', default="Inbox", help='Todoist project')

    parser.add_argument('--min-date', dest='min_date', action='store', default=None,
                        help="Earliest date you're interested in (inclusive). Format: [YYYY-MM-DD]")
    parser.add_argument('--max-date', dest='max_date', action='store', default=None,
                        help="Latest date you're interested in (inclusive). Format: [YYYY-MM-DD]")

    parser.add_argument('--team', dest='teams', action='append', default=[], help="Teams you're interested in.")

    parser.add_argument('--dry-run', dest='dry_run', action='store_true', default=False, help='No tasks will be added')
    parser.add_argument('--verbose', '-v', dest='verbose', action='store_true', default=False, help='Change log level to DEBUG')

    return parser


def get_filters(args):
    filters = []

    if args.teams:
        filters.append(TeamNameFilter(args.teams))

    if args.min_date or args.max_date:
        filters.append(DateFilter(min=args.min_date, max=args.max_date))

    return filters


def run():
    args = get_parser().parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    todoclient_config = ToDoClientConfiguration(args.username, args.password, args.project, dry_run=args.dry_run)
    filters = get_filters(args)

    rtm = RememberTheMatch(todoclient_config, filters)
    rtm.run()


def execute():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    run()
    sys.exit(0)


if __name__ == "__main__":
    execute()

