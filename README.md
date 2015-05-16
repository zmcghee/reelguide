# Treeclimber

*By Zack McGhee for Cox Media Group and Fans 1st Media*

## Overview

Treeclimber is a Django app designed to help you dynamically spin up and terminate AWS instances and run scripts on those instances.

For example, Fans 1st Media uses it to deploy WordPress installations using vip-quickstart, load a copy of production data onto that instance, and then checkout a specific branch in our theme repo and activate that theme on the installation.

You can install it as a standalone Django project, or include it as a requirement in a larger Django project.


### Local development

To begin local development, you will need:

* Git
* Python 2.7 (as specified in runtime.txt)
* pip (```easy_install pip```)
* virtualenv (```pip install virtualenv```)

Project-specific requirements for your virtualenv are captured in requirements.txt. (If you have pip, you don't need to worry about those yet.)


#### First time

Once you have Git, Python, pip, and virtualenv, ``cd`` to a directory you can work in and clone the treeclimber repo. ``cd`` into the repo.

First, create a secret.py file in the conf directory that contains a ``SECRET_KEY`` variable.

Then run:

```shell
virtualenv venv && source venv/bin/activate
python manage.py test
```

This creates and activates your virtualenv. Then it runs the test suite. If the tests pass, you're off to the races!

#### Every time

If you've already run your environment before, open your shell, CD to your django-treeclimber directory, and just activate your virtualenv:

```shell
source venv/bin/activate
```

#### Updating your repo

```shell
git pull
python manage.py test
```
