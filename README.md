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
* filter matches by team name for multiple teams (`--team`)
* filter matches in which both teams are on the provided list (`--only-these-teams` trigger)

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

Real-life usage example
-----------------------

I'm a big Premier League fan. I like some teams more, but in general I'm interested in all matches between the 6 or 7 top teams and I want to add all these matches to my Todoist "Matches" project. This is how I use this app to do what I want:

```bash
rtm --username <login> --password <password> --project Matches --team Arsenal --team "Man Utd" --team Liverpool --team Chelsea --team "Man City" --team Spurs --team Everton --only-these-teams --dry-run
```

Of course, just in case, I added `--dry-run` to make sure that I really got what I wanted.  

Note that:
* some teams have a bit different names that you would expect - there's no Tottenham: they're called "Spurs" (at the same time Chelsea is Chelsea, not "The Blues", which is a bit inconsistent)
* if team's name contains space ("Man Utd"), it's necessary to use quotation marks
* comparisons of team names are case insensitive ("Liverpool" and "liVeRpOOl" are equal)
* project needs to exist prior to adding matches

Filters
-------

### Team Name filter

You can enable filtering by team name by providing at least one team name using `--team` argument. You can provide as many team names as you want. By default filter will filter out all the matches where none of the teams' name exists on the list you provided. When `--only-these-teams`` trigger is set, **both** teams playing need to be on your list. E.g. if you support just a single team and you want to watch all its matches, you probably don't want to use that trigger. If you like to watch all the matches between "Top X" teams, you probably want to combine these team's names with that trigger.

### Date filter

You can enable filtering by date by using one or both of the `--min-date` and `--max-date` arguments. Date format is: YYYY-MM-DD, e.g. 2014-08-31. Date ranges are inclusive, which means that e.g. setting `--max-date` to 2014-08-31 will filter out all the matches that are scheduled to September and later, but will **include** matches played on 31st of August (if any).

Roadmap
-------

Current goals:
* support Remember The Milk
* support other productivity / TODO apps (Wunderlist?)

Mid-term goals:
* support Remember The Milk
* support Wunderlist
* support Primera Division
* support Champions League

Long term goals:
* interactive mode (pick matches you want to add manually from the pre-filtered list of your choice)
* support all major European leagues
* support all major task management apps

