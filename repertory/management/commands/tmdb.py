from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from repertory.utils.calendar import CalendarImport
from repertory.utils.spreadsheet import GoogleSheet

import tmdbsimple as tmdb
tmdb.API_KEY = settings.TMDB_API_KEY

class Command(BaseCommand):
    help = 'Finds TMDB data for the Google Sheet specified in settings'
    _tmdb_matches = {}
    _tmdb_askonce = False

    def handle(self, *args, **options):
        if not hasattr(settings, 'GOOGLE_SHEET_ID'):
            raise CommandError("No GOOGLE_SHEET_ID in settings file")

        # Get Google Sheet
        sheet = GoogleSheet(settings.GOOGLE_SHEET_ID)

        # Attempt to load TMDb data where applicable
        items = self.get_items_with_tmdb(sheet.items)

        # Print results
        self.stdout.write("Printing TMDb IDs in spreadsheet order for you "\
        "to copy and paste:")
        for item in items:
            print item['tmdb']
        self.stdout.write("All done!")

    def get_items_with_tmdb(self, items):
        """Interactive attempt to load TMDb data where applicable"""
        self.stdout.write("Attempting to find TMDb data where applicable")
        user_tmdb_rule = raw_input("Should I assume repeat titles are "\
          "the same? (y/n): ")
        if user_tmdb_rule[:1].strip().lower() == 'y':
            self._tmdb_askonce = True
        processed = []
        for item in items:
            if item.get('tmdb', ''): # The item dict already has a TMDB ID
                processed.append(item)
                continue
            item['tmdb'] = "" # default
            if self._tmdb_askonce and item['title'] in self._tmdb_matches:
                item['tmdb'] = self._tmdb_matches.get(item['title'])
            else:
                item['tmdb'] = self.get_tmdb_option_from_user(item)
            if item['title'] not in self._tmdb_matches:
                self._tmdb_matches.update({item['title']: item['tmdb']})
            processed.append(item)
        return processed

    def get_tmdb_option_from_user(self, item, q=False):
        search = tmdb.Search()
        if not q:
            search_term = item['title']
            if item['title'].__contains__(" w/"):
                search_term = item['title'].split(" w/")[0]
        else:
            search_term = q
        response = search.movie(query=search_term)
        result_count = len(search.results)
        if not q and result_count < 1:
            if item['title'].__contains__(":"):
                split_colon = item['title'].split(":", 1)
                search_term = split_colon[0]
                response = search.movie(query=search_term)
                result_count = len(search.results)
                if result_count < 1:
                    search_term = split_colon[1]
                    response = search.movie(query=search_term)
                    result_count = len(search.results)
        question = u"Please choose an option for %s at %s on %s:\n"\
          % (item['title'], item['venue'], item['date'])
        for i in range(0, result_count):
            movie = search.results[i]
            question += "%s. %s (%s)\n" % (i, movie['title'],
              movie['release_date'][:4])
        question += "%s. Enter a new search term\n" % result_count
        question += "%s. None of the above\n" % (result_count + 1)
        question += "Choice: "
        answer = result_count + 2
        while answer > (result_count + 1):
            answer = raw_input(question.encode('utf-8'))
            try:
                answer = int(answer)
            except:
                pass
        if answer < result_count:
            return search.results[answer]['id']
        if answer == result_count:
            search_term = raw_input("New search term: ")
            return self.get_tmdb_option_from_user(item, q=search_term)
        return raw_input("Enter TMDb ID (can be blank): ")