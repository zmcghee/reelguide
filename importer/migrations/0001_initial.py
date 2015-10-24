# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repertory', '0009_auto_20150824_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('venues', models.ManyToManyField(to='repertory.Venue')),
            ],
        ),
    ]
