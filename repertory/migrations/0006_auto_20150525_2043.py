# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repertory', '0005_auto_20150522_0722'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventinstance',
            options={'ordering': ['datetime']},
        ),
        migrations.RemoveField(
            model_name='event',
            name='imdb',
        ),
        migrations.RemoveField(
            model_name='reeluser',
            name='fb_cache',
        ),
    ]
