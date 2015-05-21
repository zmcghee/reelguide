import json
import requests

class GoogleSheet(object):
    sheet_id = None
    fields = []

    def __init__(self, sheet_id, fields=[], fetch=True):
        self.sheet_id = sheet_id
        if fields: # before fetch in case fetch fails
            self.set_fields(fields)
        if fetch:
            self.fetch()
            if not fields and fields != False:
                # after fetch so we can infer from data
                self.auto_fields()

    @property
    def json_url(self):
        url = 'https://spreadsheets.google.com/feeds/list/'\
            + '%s/default/public/values?alt=json' % (self.sheet_id)
        return url

    def fetch(self):
        self._google = requests.get(self.json_url)
        if self._google.status_code != 200:
            raise Exception("Google Sheet returned non-200 response")
        self.gsx = self._google.json()

    def set_fields(self, fields):
        self.fields = fields

    def auto_fields(self):
        try:
            keys = self.gsx['feed']['entry'][0].keys()
        except IndexError:
            pass
        else:
            fields = []
            for key in keys:
                if key.startswith('gsx$'):
                    fields.append(key)
            self.set_fields(fields)

    @property
    def items(self, fields=[]):
        if fields:
            self.set_fields(fields)
        items = []
        for entry in self.gsx['feed']['entry']:
            item = {}
            for field in self.fields:
                if field.startswith('gsx$'):
                    gsx_key = field
                else:
                    gsx_key = 'gsx$' + field
                key = gsx_key[4:]
                item[key] = entry[gsx_key]['$t']
            items.append(item)
        return items