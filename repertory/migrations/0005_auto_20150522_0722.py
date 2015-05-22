# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repertory', '0004_remove_reeluser_first_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reeluser',
            name='facebook_id',
            field=models.CharField(max_length=100),
        ),
    ]
