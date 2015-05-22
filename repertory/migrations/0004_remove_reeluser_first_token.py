# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repertory', '0003_auto_20150522_0123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reeluser',
            name='first_token',
        ),
    ]
