from django.core.management.base import BaseCommand

from repertory.models.users import ReelUser
from repertory.utils.ical import ics_for_user

class Command(BaseCommand):
    help = 'Regenerates cache for all users iCal feeds'

    def handle(self, *args, **options):
        exceptions = []
        count = 0
        for ru in ReelUser.objects.all():
            try:
                o = ics_for_user(ru, refresh=True)
            except:
                exceptions.append(ru)
            else:
                count += 1
        msg = "Done! Updated %s users. Failed for these %s users: [%s]" % (
          count, len(exceptions), ", ".join(exceptions))
        self.stdout.write(msg)