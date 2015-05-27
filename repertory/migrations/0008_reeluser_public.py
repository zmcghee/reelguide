# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repertory', '0007_reeluser_ical'),
    ]

    operations = [
        migrations.AddField(
            model_name='reeluser',
            name='public',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
