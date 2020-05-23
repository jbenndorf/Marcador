from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Bookmark, Tag


class TagTestCase(TestCase):
    def test_str(self):
        tag = Tag.objects.create(name='test')
        self.assertEqual(str(tag), 'test')


class BookmarkTestCase(TestCase):
    fixtures = ['user']

    def test_str(self):
        bookmark = Bookmark.objects.create(
            bookmark_url='http://localhost:8000',
            title='localhost',
            owner=User.objects.get(pk=1),
        )
        self.assertEqual(str(bookmark), 'localhost (http://localhost:8000)')

    def test_save(self):
        bookmark = Bookmark.objects.create(
            bookmark_url='http://localhost:8000',
            title='localhost',
            owner=User.objects.get(pk=1),
        )
        self.assertIsInstance(bookmark.date_created, datetime)
        self.assertIsInstance(bookmark.date_updated, datetime)
