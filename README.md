Remember The Match
==================

Never forget about an important match by automatically adding it to your task management app!

Features
--------

Supported Leagues:
* Premier League schedule (http://www.premierleague.com)

Supported "TODO" / productivity apps:
* Todoist app (http://todoist.com)

It is possible to:
* filter matches by date (`--min-date` and `--max-date`)
* filter matches by team name for multiple teams (`--team` trigger)

See Filters for details.

Running the app
---------------

Run the tests:

```bash
python setup.py test
```

Install:

```bash
python setup.py install
```

Run the app using your Todoist account credentials:

```bash
rtm --username <login> --password <password> --dry-run
```

Remove `--dry-run` to make it actually work

Or check out help:

```bash
rtm --help
```

Filters
-------

TODO

Roadmap
-------

Current goals:
* add matches between given teams (not only: all matches of given teams)

Mid-term goals:
* support Remember The Milk
* support Wunderlist
* support Primera Division
* support Champions League

Long term goals:
* interactive mode (pick matches you want to add manually from the pre-filtered list of your choice)
* support all major European leagues
* support all major task management apps

