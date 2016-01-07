import json
import gspread

from django.conf import settings
from oauth2client.client import SignedJwtAssertionCredentials

def gc():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(settings.GOOGLE_CLIENT_EMAIL, settings.GOOGLE_PRIVATE_KEY, scope)
    ss = gspread.authorize(credentials)
    return ss

def send_rows_to_sheet(sheet_key, cols, rows, useSheet1=True):
    ss = gc().open_by_key(sheet_key)
    if useSheet1:
        wks = ss.sheet1
    else:
        wks.add_worksheet("Import Export", len(rows), len(cols))
        wks.append_row(cols)
    for row in rows:
        wks.append_row(row)