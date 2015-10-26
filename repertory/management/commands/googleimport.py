from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from repertory.utils.calendar import CalendarImport
from repertory.utils.spreadsheet import GoogleSheet

from importer.models import DataSource

class Command(BaseCommand):
    help = 'Imports data from the Google Sheets in the DataSource model'

    def handle(self, *args, **options):
        if DataSource.objects.count() < 1:
            raise CommandError("No data sources found.")

        all_items = []

        # Get Google Sheets
        for data in DataSource.objects.all():
            sheet = GoogleSheet(data.sheet_id)
            all_items += sheet.items
            self.stdout.write("Found %s items for %s." % (len(sheet.items), data))

        # Prepare calendar import
        cal = CalendarImport(all_items)
        cal.prepare()
        self.stdout.write(cal.human_readable_prep_result)
        if len(cal.delete) > 0:
            self.stdout.write("To be deleted: %s" % cal.delete)

        user_continue = raw_input("Continue? (y/n): ")
        if user_continue[:1].strip().lower() != 'y':
            self.stdout.write("Stopping.")
            return

        self.stdout.write("Running import...")
        cal.run()
        self.stdout.write("Import done. Result:")
        self.stdout.write(cal.human_readable_run_result)