import requests

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