# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('tmdb', models.PositiveIntegerField(null=True, blank=True)),
                ('imdb', models.PositiveIntegerField(null=True, blank=True)),
                ('sort_title', models.CharField(max_length=250, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('format', models.CharField(default=b'Unknown', max_length=20, db_index=True)),
                ('is_film', models.BooleanField(default=False)),
                ('url', models.URLField(null=True, blank=True)),
                ('event', models.ForeignKey(related_name='instances', to='repertory.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='eventinstance',
            name='series',
            field=models.ForeignKey(related_name='events', blank=True, to='repertory.Series', null=True),
        ),
        migrations.AddField(
            model_name='eventinstance',
            name='venue',
            field=models.ForeignKey(related_name='events', to='repertory.Venue'),
        ),
    ]
