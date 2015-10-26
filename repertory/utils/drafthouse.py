"""
from repertory.utils.drafthouse import AlamoDrafthouse, LOCATIONS
for theater_id, theater_name in LOCATIONS:
    theater = AlamoDrafthouse(theater_id)
    theater.fetch()
    theater.parse_html()
    theater.auto()
"""

import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

LOCATIONS = (
    ('0002', 'Alamo Ritz'),
    ('0003', 'Alamo Village'),
    ('0004', 'Alamo South Lamar'),
    ('0006', 'Alamo Slaughter Lane'),
    ('0007', 'Alamo Lakeline')
)

class AlamoDrafthouse(object):
    def __init__(self, calendar_id):
        self.calendar_id = calendar_id
        self.events = {}
        self.lookup = {}
        self.ignore = {}

    @property
    def ajax_calendar_url(self):
        return 'https://drafthouse.com/ajax/.showtimes-calendar/%s' % self.calendar_id

    def fetch(self):
        self._req = requests.get(self.ajax_calendar_url)
        if self._req.status_code != 200:
            raise Exception("Alamo request returned non-200 response")
        self.ajax = self._req.text

    def parse_html(self):
        soup = BeautifulSoup(self.ajax, 'html.parser')
        calendars = soup.find_all("section", "Calendar")
        for calendar in calendars:
            days = calendar.find_all("div", "Calendar-day")
            for day in days:
                try:
                    date = day.find("div", "Calendar-date").text
                except AttributeError:
                    continue
                shows = day.find_all("p")
                for show in shows:
                    evt = show.find("strong", "Calendar-show")
                    event_name = evt.text
                    event_link = evt.find("a", href=True)['href']
                    event_times = []
                    tms = show.find_all("a", "Calendar-time", href=True)
                    for tm in tms:
                        event_times.append((date, tm.text, tm['href'].replace(
                            'ajax/.showtimes-session-modal', 'ticketing')))
                    if event_link not in self.events:
                        self.events[event_link] = {}
                    self.events[event_link]['name'] = event_name
                    if 'schedule' not in self.events[event_link]:
                        self.events[event_link]['schedule'] = []
                    self.events[event_link]['schedule'] += event_times

    def auto(self):
        for link, event in self.events.iteritems():
            series, title = self.suss_out_title(event['name'])
            ignore = self.ignore_event(series, title, len(event['schedule']))
            if not ignore:
                self.lookup[link] = event
                self.lookup[link]['title'] = title
                self.lookup[link]['series'] = series
            else:
                self.ignore[link] = event
                self.ignore[link]['title'] = title
                self.ignore[link]['series'] = series

    def all_ignore_to_lookup(self):
        for link, event in self.ignore.iteritems():
            self.ignore_to_lookup(link)

    def ignore_to_lookup(self, link):
        if link in self.lookup:
            self.lookup[link]['schedule'] += self.ignore[link]['schedule']
        else:
            self.lookup[link] = self.ignore[link]

    def ignore_event(self, series, title, show_count):
        s = series.lower() if series else ""
        t = title.lower()
        if t.endswith("qal") or t.endswith("quote-along")\
          or s=='master pancake' or t=='choose your own pancake'\
          or show_count > 6\
          or (s.endswith("action pack") and t.endswith("party")):
            return True
        return False

    def suss_out_title(self, event_name, articles=['a', 'an', 'of', 'the', 'with']):
        m = re.search('^([A-Z][a-z].*): (.*)$', event_name)
        if m:
            series = m.group(1).encode('utf-8')
            title = m.group(2).encode('utf-8')
        else:
            series = None
            title = event_name.encode('utf-8')
        if title.startswith("2D ") or title.startswith("3D "):
            new_title = title[3:]
            format = title[:2]
        else:
            new_title = title
            format = None
        word_list = re.split(' ', new_title)
        final = [word_list[0].capitalize()]
        for word in word_list[1:]:
            final.append(word in articles and word or word.capitalize())
        new_title = " ".join(final)
        if format:
            title = "%s (%s)" % (new_title, format)
        else:
            title = new_title
        return (series, title)