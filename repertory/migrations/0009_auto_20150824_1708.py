# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repertory', '0008_reeluser_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reeluser',
            name='public',
            field=models.CharField(max_length=100, unique=True, null=True, blank=True),
        ),
    ]
