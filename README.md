# Reel Guide

*A social repertory cinema calendar by Zack McGhee*

## Overview

Reel Guide is a Django project designed to provide repertory cinema listings, as well as some lightweight social functionality around those listings.

Pull requests welcome.

### Local development

To begin local development, you will need:

* Git
* Python 2.7 (as specified in runtime.txt)
* pip (```easy_install pip```)
* virtualenv (```pip install virtualenv```)

Project-specific requirements for your virtualenv are captured in requirements.txt. (If you have pip, you don't need to worry about those yet.)


#### First time

Once you have Git, Python, pip, and virtualenv, ``cd`` to a directory you can work in and clone the reelguide repo. ``cd`` into the repo.

First, create a secret.py file in the conf directory that contains a ``SECRET_KEY`` variable.

Then run:

```shell
virtualenv venv && source venv/bin/activate
python manage.py test conf.tests
```

This creates and activates your virtualenv. Then it runs the test suite. If the tests pass, you're off to the races!

#### Every time

If you've already run your environment before, open your shell, CD to your reelguide directory, and just activate your virtualenv:

```shell
source venv/bin/activate
```

#### Updating your repo

```shell
git pull
python manage.py test
```

#### Loading data

There are two options for loading data into your environment.

##### Fixture

The event calendar every week with the third week out. When that happens, I'll update a fixture file in this repo called events. You can load it like this:

```shell
python manage.py loaddata events
```

##### Management command

There's also a management command to load data from the current Google Sheet. That's where calendar info. originates. This command will take that spreadsheet data and (optionally) do a TMDB lookup, in addition to mapping other event info. to the database.

```shell
python manage.py googleimport
```

I run this command locally to stage the weekly calendar update. Then I generate the fixture file above and use that to update the data in production. To generate the fixture file, I run:

```shell
python manage.py dumpdata repertory.Event repertory.Venue \
repertory.Series repertory.EventInstance --indent 4 > events.json
```