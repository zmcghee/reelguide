from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=250)
    tmdb = models.PositiveIntegerField(null=True, blank=True)
    imdb = models.PositiveIntegerField(null=True, blank=True)
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

class Venue(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class Series(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'series'

    def __unicode__(self):
        return self.name

class EventInstance(models.Model):
    event = models.ForeignKey(Event, related_name='instances')
    venue = models.ForeignKey(Venue, related_name='events')
    datetime = models.DateTimeField()
    format = models.CharField(max_length=20, default='Unknown',
      db_index=True)
    is_film = models.BooleanField(default=False, blank=True)
    series = models.ForeignKey(Series, null=True, blank=True,
      related_name='events')
    url = models.URLField(null=True, blank=True)