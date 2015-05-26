# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repertory', '0006_auto_20150525_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='reeluser',
            name='ical',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
