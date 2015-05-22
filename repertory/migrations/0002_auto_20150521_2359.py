# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repertory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReelUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('facebook_id', models.PositiveIntegerField()),
                ('fb_token', models.CharField(max_length=250, blank=True)),
                ('first_token', models.CharField(max_length=250)),
                ('fb_cache', models.TextField(blank=True)),
                ('event_instances', models.ManyToManyField(related_name='attendees', to='repertory.EventInstance', blank=True)),
                ('user', models.OneToOneField(related_name='reeluser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='series',
            options={'verbose_name_plural': 'series'},
        ),
    ]
