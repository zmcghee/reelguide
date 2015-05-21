from django.test import TestCase
from repertory.models import Event

class EventModelTestCase(TestCase):
    def setUp(self):
        self.instance = Event.objects.create(title='My event')

    def test_model_fields(self):
        """Lookup setUp instance and check fields"""
        instance = Event.objects.all()[0]
        self.assertEqual(instance.title, 'My event')
        self.assertEqual(instance.tmdb, None)

    def test_sort_title_with_leading_article(self):
        """On save, a model should get a sort_title"""
        instance = Event(title="The Test Event")
        self.assertEqual(instance.sort_title, '')
        instance.save()
        self.assertEqual(instance.sort_title, 'Test Event')

    def test_sort_title_without_leading_article(self):
        """On save, a model should get a sort_title"""
        instance = Event(title="My Test Event")
        self.assertEqual(instance.sort_title, '')
        instance.save()
        self.assertEqual(instance.sort_title, 'My Test Event')