import requests

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from repertory.models.events import EventInstance

class ReelUser(models.Model):
    user = models.OneToOneField(User, related_name='reeluser')
    facebook_id = models.PositiveIntegerField()
    event_instances = models.ManyToManyField(EventInstance, blank=True,
      related_name='attendees')
    fb_token = models.CharField(max_length=250, blank=True)
    first_token = models.CharField(max_length=250)
    fb_cache = models.TextField(blank=True)

    @property
    def event_ids(self):
        return self.event_instances.values_list('pk', flat=True)

    @property
    def calendar(self):
        items = []
        filter = {'datetime__gte': datetime.now()}
        qs = self.event_instances.filter(**filter).order_by('datetime')
        for event in qs:
            items.append(event.as_dict)
        return items