from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from repertory.utils.drafthouse import AlamoDrafthouse, LOCATIONS

class Command(BaseCommand):
    help = 'Imports data from the Alamo Drafthouse'

    def handle(self, *args, **options):
        rows = []

        for theater_id, theater_name in LOCATIONS:
            self.stdout.write("Starting %s..." % theater_name)
            theater = AlamoDrafthouse(theater_id)
            theater.fetch()
            theater.parse_html()
            theater.auto()

            ignored = "I think we should ignore these items. Does this look right?\n"
            for link, event in theater.ignore.iteritems():
                ignored += "%s\n" % event['name']
            ignored += 'y/n: '
            answer = False
            while answer not in ['y', 'n']:
                answer = raw_input(ignored).strip().lower()

            if answer == 'n':
                theater.all_ignore_to_lookup()

            for link, event in theater.lookup.iteritems():
                if len(event['schedule']) < 1:
                    self.stdout.write("Skipping %s cuz no shows." % event['name'])
                    continue
                question = "Leave blank to use %s (%s). " % (event['title'], event['series'])
                question += "Type 1 to retype, 2 to ignore. "
                answer = raw_input(question).strip().lower()
                if answer == "1":
                    title = raw_input("New title: ")
                elif answer == "2":
                    continue
                else:
                    title = event['title']
                for date, time, ticketing in event['schedule']:
                    rows.append([date, time, title, theater_name, "",
                      event['series'] or "", "", ticketing])

        for row in rows:
            self.stdout.write("\t".join(row))
