from django.db import models
from repertory.models import Venue

class DataSource(models.Model):
    url = models.URLField()
    venues = models.ManyToManyField(Venue)

    def __unicode__(self):
        return ", ".join(self.venues.values_list('name', flat=True))

    @property
    def sheet_id(self):
        if self.url.__contains__("spreadsheets/d"):
            parts = self.url.split("/", 7)
            if parts[4] == 'd':
                return parts[5]
        return None