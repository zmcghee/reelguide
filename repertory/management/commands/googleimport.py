from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from repertory.utils.calendar import CalendarImport
from repertory.utils.spreadsheet import GoogleSheet

class Command(BaseCommand):
    help = 'Imports data from the Google Sheet specified in settings'
    _tmdb_matches = {}
    _tmdb_askonce = False

    def handle(self, *args, **options):
        if not hasattr(settings, 'GOOGLE_SHEET_ID'):
            raise CommandError("No GOOGLE_SHEET_ID in settings file")

        # Get Google Sheet
        sheet = GoogleSheet(settings.GOOGLE_SHEET_ID)

        # Prepare calendar import
        cal = CalendarImport(sheet.items)
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