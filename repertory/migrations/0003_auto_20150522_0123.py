# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repertory', '0002_auto_20150521_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventinstance',
            name='datetime',
            field=models.DateTimeField(db_index=True),
        ),
    ]
