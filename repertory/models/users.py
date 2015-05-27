import base64
import requests
import uuid

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from repertory.models.events import EventInstance

class ReelUser(models.Model):
    user = models.OneToOneField(User, related_name='reeluser')
    facebook_id = models.CharField(max_length=100)
    event_instances = models.ManyToManyField(EventInstance, blank=True,
      related_name='attendees')
    fb_token = models.CharField(max_length=250, blank=True)
    ical = models.CharField(max_length=250, null=True, blank=True)
    public = models.CharField(max_length=100, null=True, blank=True)

    @property
    def event_ids(self):
        return self.event_instances.values_list('pk', flat=True)

    def calendar(self, *args, **kwargs):
        items = []
        filter = {'datetime__gte': datetime.now()}
        qs = self.event_instances.filter(**filter).order_by('datetime')
        for event in qs:
            items.append(event.as_dict(**kwargs))
        return items

    def set_ical_key(self):
        key = base64.b64encode(uuid.uuid4().bytes).replace('=', '')
        self.ical = key.encode('ascii')