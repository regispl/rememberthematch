Remember The Match
==================

Never forget about an important match by automatically adding it to your task management app!

Run the tests:

```bash
./bin/nosetests
```

Run the app using your Todoist account credentials:

```bash
./bin/rtm --username <login> --password <password>
```

Or check out help:

```bash
./bin/rtm --help
```

At the moment application supports:
* Premier League schedule (http://www.premierleague.com)
* Todoist app (http://todoist.com)

Currently it's only possible to add all matches of a season, which is not extremally useful, but it will change soon.

Current goals:
* match filtering based on team name (names)
* add all matches between given teams

Mid-term goals:
* support Remember The Milk
* support Primera Division
* support Champions League

Long term goals:
* support all major European leagues
* support all major task management apps

;-)
