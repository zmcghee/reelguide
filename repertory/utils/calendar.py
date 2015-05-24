from datetime import datetime, timedelta
from repertory.models import Event, Venue, Series, EventInstance

class CalendarImport(object):
    """Expects a list of Python dicts with the keys `title` (str),
    `date` (str in format 'Thu 5/21/2015'), `time` (str in format
    '7:30 PM'), `venue`, `series`, `format`, `tmdb` and `imdb`
    (all strings, can be empty). Usage:
    
        >>> cal = CalendarImport(myitems)
        >>> cal.prepare()
        >>> print cal.human_readable_prep_result
        
    """
    items = []
    ignored = []
    create = []
    modify = []
    update = []
    delete = []

    def __init__(self, items):
        self.items = items

    def get_event_for_item(self, item):
        # Not all events are movies or have TMDb info
        if not item.get('tmdb', ''):
            event, c = Event.objects.get_or_create(title=item['title'])
            return event
        # ...but, of course, lots are
        try:
            event = Event.objects.get(tmdb=item['tmdb'])
        except Event.DoesNotExist:
            event = Event(title=item['title'], tmdb=item['tmdb'])
        if item.get('imdb', ''):
            event.imdb = item['imdb']
        event.save()
        return event

    def get_venue_for_item(self, item):
        if not item.get('venue', ''):
            return None
        venue, c = Venue.objects.get_or_create(name=item['venue'])
        return venue

    def get_series_for_item(self, item):
        if not item.get('series', ''):
            return None
        series, c = Series.objects.get_or_create(name=item['series'])
        return series

    def get_is_film_bool_for_item(self, item):
        if not item.get('format', None):
            return False
        return item['format'].endswith('mm')

    def get_datetime_for_item(self, item):
        if not item.get('date', '') or not item.get('time', ''):
            return None
        format = "%a %m/%d/%Y %I:%M %p" # e.g. Thu 5/21/2015 7:30 PM
        date_string = "%s %s" % (item['date'], item['time'])
        try:
            return datetime.strptime(date_string, format)
        except:
            return None

    def prepare(self):
        """This method takes the items you submit, finds or creates
        the requisite Event, Venue, and Series objects, but does
        not yet modify the EventInstance table, instead queueing
        those tasks for your review and approval."""
        # We need these for later
        still_valid_ids = []
        now = datetime.now()
        # Iterate through calendar items to be imported
        for item in self.items:
            # Get datetime for item
            item_datetime = self.get_datetime_for_item(item)
            # Append to ignored items if no date/time or event past
            if not item_datetime:
                self.ignored.append((item, "No date/time info"))
                continue
            if item_datetime < now:
                self.ignored.append((item, "Event already happened"))
            # Get everything we need for an EventInstance
            prepared = {
                'datetime': item_datetime,
                'event': self.get_event_for_item(item),
                'venue': self.get_venue_for_item(item),
                'series': self.get_series_for_item(item),
                'is_film': self.get_is_film_bool_for_item(item),
                'format': item.get('format', ''),
            }
            # Does this instance already exist?
            try:
                obj = EventInstance.objects.get(event=prepared['event'],             
                  venue=prepared['venue'], datetime=prepared['datetime'])
            except EventInstance.DoesNotExist:
                try:
                    # Find an event instance with this name at this venue
                    # within an hour (time may have changed slightly)
                    obj = EventInstance.objects.get(event=prepared['event'],             
                      venue=prepared['venue'],
                      datetime__gte=(prepared['datetime'] - timedelta(hours=1)),
                      datetime__lte=(prepared['datetime'] + timedelta(hours=1)),
                    )
                except EventInstance.DoesNotExist, EventInstance.MultipleObjectsReturned:
                    # If not, add it to list of objs to be created
                    self.create.append(prepared)
                else:
                    # if so, assume the time just changed slightly
                    self.modify.append((obj, prepared))
                    still_valid_ids.append(obj.pk)
            else:
                # If it does exist, add it to list of objs to update
                self.update.append((obj, prepared))
                # Also add its ID to a list of still-valid future objs
                still_valid_ids.append(obj.pk)
        # Now we need to collect the IDs of future events that no
        # longer appear to be valid (they're in the db, but not items)
        self.delete = EventInstance.objects.filter(datetime__gte=now
          ).exclude(pk__in=still_valid_ids)

    @property
    def human_readable_prep_result(self):
        return """Prep results:
%s items ignored.
%s items will be created.
%s items will be modified.
%s items will be deleted.
%s items look unchanged but will be updated.""" % (len(self.ignored), len(self.create),
          len(self.modify), len(self.delete), len(self.update))

    @property
    def human_readable_run_result(self):
        return """Run results:
%s of %s items created.
%s of %s items modified.
%s of %s items deleted.
%s of %s items looked unchanged but were updated.""" % (len(self.created), len(self.create),
          len(self.modified), len(self.modify), self.deleted, 
          len(self.delete), len(self.updated), len(self.update))

    def run(self):
        self.deleted = self.process_delete()
        self.updated = self.process_update()
        self.modified = self.process_modify()
        self.created = self.process_create()

    def process_create(self):
        created = []
        for prepared in self.create:
            obj = EventInstance(**prepared)
            obj.save()
            created.append(obj)
        return created

    def process_update(self):
        updated = []
        for obj, prepared in self.update:
            obj.datetime = prepared['datetime']
            obj.series = prepared['series']
            obj.is_film = prepared['is_film']
            obj.format = prepared['format']
            obj.save()
            updated.append(obj)
        return updated

    def process_modify(self):
        modified = []
        for obj, prepared in self.modify:
            obj.datetime = prepared['datetime']
            obj.series = prepared['series']
            obj.is_film = prepared['is_film']
            obj.format = prepared['format']
            obj.save()
            modified.append(obj)
        return modified

    def process_delete(self):
        deleted = 0
        for obj in self.delete.all():
            # Iterate through the list rather than bulk delete
            # in case we want to use delete signals at some point
            obj.delete()
            deleted = deleted + 1
        return deleted