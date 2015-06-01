from datetime import timedelta

from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=250)
    tmdb = models.PositiveIntegerField(null=True, blank=True)
    sort_title = models.CharField(max_length=250, blank=True)

    def __unicode__(self):
        return self.title

    def set_sort_title(self):
        articles = ('the', 'a', 'an', 'le', 'la')
        self.sort_title = self.title # default
        split_title = self.title.split()
        if len(split_title) > 1:
            if split_title[0].lower() in articles:
                self.sort_title = self.title.split(' ', 1)[1]

    def save(self, *args, **kwargs):
        self.set_sort_title()
        return super(Event, self).save(*args, **kwargs)

class Venue(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    @property
    def as_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'notes': self.notes
        }

class Series(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'series'

    def __unicode__(self):
        return self.name

    @property
    def as_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'notes': self.notes
        }

class EventInstance(models.Model):
    event = models.ForeignKey(Event, related_name='instances')
    venue = models.ForeignKey(Venue, related_name='events')
    datetime = models.DateTimeField(db_index=True)
    format = models.CharField(max_length=20, default='Unknown',
      db_index=True)
    is_film = models.BooleanField(default=False, blank=True)
    series = models.ForeignKey(Series, null=True, blank=True,
      related_name='events')
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['datetime']

    def __unicode__(self):
        return "%s at %s on %s" % (self.event, self.venue, self.datetime)

    def save(self, *args, **kwargs):
        result = super(EventInstance, self).save(*args, **kwargs)
        self.update_ical_for_attendees()
        return result

    def as_dict(self, python_datetime=False):
        datetime_format = "%Y-%m-%d %H:%M:00"
        sort_dt_fmt = "%Y%m%d%H%M"
        obj = {
            'title': self.event.title,
            'tmdb': self.event.tmdb,
            'event_id': self.event.id,
            'event_instance_id': self.id,
            'venue': self.venue.as_dict,
            'external_url': self.url,
            'is_film': self.is_film,
            'format': self.format,
            'datetime': self.datetime.strftime(datetime_format),
            'sort_title': self.event.sort_title,
            'sort_datetime': self.datetime.strftime(sort_dt_fmt),
        }
        obj['datetime_unconfirmed'] = obj['sort_datetime'][-1] in ('1','6')
        obj['series'] = None if not self.series else self.series.as_dict
        if python_datetime:
            obj['datetime'] = self.datetime
            obj['endtime'] = self.datetime + timedelta(hours=2)
        return obj

    def update_ical_for_attendees(self):
        from repertory.utils.ical import ics_for_user
        for reeluser in self.attendees.all():
            ics = ics_for_user(reeluser, action='update', event_instance=self)