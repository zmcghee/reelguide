from django.test import TestCase
from repertory.utils.spreadsheet import GoogleSheet

class GoogleSheetTestCase(TestCase):
    def setUp(self):
        sheet_id = '1PWhG8sLvoGM86OTBPIc7lrWYnqoAQPo9hzrEJRnKogE'
        self.sheet = GoogleSheet(sheet_id, fetch=True, fields=False)

    def test_fetch(self):
        """Google should return a 200 response"""
        self.assertEqual(self.sheet._google.status_code, 200)

    def test_auto_fields(self):
        """Test introspection of fields from Google Sheet"""
        self.assertEqual(len(self.sheet.fields), 0)
        self.sheet.auto_fields()
        self.assertEqual(len(self.sheet.fields), 6)