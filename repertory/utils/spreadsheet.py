import json
import requests

class GoogleSheet(object):
    """
    Class to import the first sheet of a Google Sheet and
    convert it to a Python dictionary. Basic usage:
    
        >>> sheet_id = '1PWhG8sLvoGM86OTBPIc7lrWYnqoAQPo9hzrEJRnKogE'
        >>> sheet = GoogleSheet(sheet_id)
        >>> sheet.items
    """
    sheet_id = None
    fields = []

    def __init__(self, sheet_id, fields=[], fetch=True):
        """Class will fetch the remote data and introspect fields
        from the data by default upon instantiation. You can pass
        fetch=False to disable this behavior and call them
        explicitly, such as:

            >>> sheet = GoogleSheet(sheet_id, fetch=False)
            >>> sheet.fetch()
            >>> sheet.auto_fields()
            >>> sheet.items
            [(list of dicts)...]

        You can also explicitly pass the fields you want returned,
        either here or using the set_fields method. Examples:
        
            >>> sheet = GoogleSheet(sheet_id, fields=['name', 'email'])
            >>> sheet.items.keys()
            ['name', 'email']

            >>> sheet = GoogleSheet(sheet_id, fetch=False)
            >>> sheet.set_fields(['name', 'email'])
            >>> sheet.items.keys()
            ['name', 'email']
        """
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
        """Returns a simple URL to fetch the first sheet of
        a Google Sheet in JSON format from Google"""
        url = 'https://spreadsheets.google.com/feeds/list/'\
            + '%s/default/public/values?alt=json' % (self.sheet_id)
        return url

    def fetch(self):
        """Fetch json_url, convert the JSON to Python & store it"""
        self._google = requests.get(self.json_url)
        if self._google.status_code != 200:
            raise Exception("Google Sheet returned non-200 response")
        self.gsx = self._google.json()

    def set_fields(self, fields):
        """Explicitly set fields you want from the sheet"""
        self.fields = fields

    def auto_fields(self):
        """Infer fields from keys in your sheet's first entry"""
        try:
            keys = self.gsx['feed']['entry'][0].keys()
        except KeyError, IndexError:
            pass
        else:
            fields = []
            for key in keys:
                if key.startswith('gsx$'):
                    fields.append(key)
            self.set_fields(fields)

    @property
    def items(self):
        """Returns entries from your sheet"""
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
                if isinstance(item[key], basestring):
                    item[key] = item[key].strip()
            items.append(item)
        return items