from django.contrib.auth.models import User
from django.test import TestCase

from .models import Bookmark, Tag


class BookmarkListTestCase(TestCase):
    fixtures = ['bookmark', 'tag', 'user']

    def test_public_bookmarks(self):
        """
        All public bookmarks should be listed.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['bookmarks'].count(), 2)

    def test_filter_tags(self):
        """
        List of public bookmarks should be filtered by tags.
        """
        response = self.client.get('/?tags=testtag')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['bookmarks'].count(), 1)
        self.assertIn(
            Tag.objects.get(name='testtag'),
            response.context['bookmarks'][0].tags.all()
        )


class UserBookmarkListTestCase(TestCase):
    fixtures = ['bookmark', 'tag', 'user']

    def test_unauthenticated_public_bookmarks(self):
        """
        An unauthenticated user should be able to retrieve all public
        bookmarks belonging to any user.
        """
        response = self.client.get('/user/dummy/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['bookmarks'].count(), 1)

    def test_user_all_own_bookmarks(self):
        """
        A user should be able to retrieve all of his own bookmarks.
        """
        self.client.force_login(user=User.objects.get(username='dummy'))
        response = self.client.get('/user/dummy/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['bookmarks'].count(), 2)
        self.assertEqual(
            response.context['bookmarks'].filter(is_public=False).count(),
            1
        )

    def test_superuser_all_bookmarks(self):
        """
        A superuser should be able to retrieve all public bookmarks
        belonging to any user.
        """
        self.client.force_login(user=User.objects.get(username='superuser'))
        response = self.client.get('/user/dummy/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['bookmarks'].count(), 2)


class BookmarkCreateTestCase(TestCase):
    fixtures = ['bookmark', 'tag', 'user']

    def test_create_is_protected(self):
        """
        An unauthenticated user should not be able to access the form.
        A redirect to the login page should follow up.
        """
        response = self.client.get('/create/')
        self.assertRedirects(response, '/login/?next=/create/')

    def test_user_gets_form(self):
        """
        An authenticated user should be able to access the form.
        """
        self.client.force_login(user=User.objects.get(username='dummy'))
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_user_create_bookmark(self):
        """
        An authenticated user should be able to create a bookmark.
        """
        self.client.force_login(user=User.objects.get(username='dummy'))
        response = self.client.post(
            '/create/',
            {
                'bookmark_url': 'http://localhost:8000',
                'title': 'localhost',
                'is_public': True,
                'tags': [1, 2, 3]
            }
        )
        self.assertRedirects(response, '/')
        self.assertIsInstance(Bookmark.objects.get(title='localhost'), Bookmark)


class BookmarkUpdateTestCase(TestCase):
    fixtures = ['bookmark', 'tag', 'user']

    def test_update_is_protected(self):
        """
        An unauthenticated user should not be able to access the form.
        A redirect to the login page should follow up.
        """
        response = self.client.get('/edit/1/')
        self.assertRedirects(response, '/login/?next=/edit/1/')

    def test_user_get_form(self):
        """
        An authenticated user should be able to access the form.
        """
        self.client.force_login(user=User.objects.get(username='dummy'))
        response = self.client.get('/edit/2/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_user_edit_own_bookmark(self):
        """
        An authenticated user should be able to edit own bookmarks.
        """
        self.client.force_login(user=User.objects.get(username='dummy'))
        response = self.client.post(
            '/edit/2/',
            {
                'bookmark_url': 'http://localhost:8000',
                'title': 'localhost',
                'is_public': True,
                'tags': [1, 2, 3]
            }
        )
        self.assertRedirects(response, '/')
        self.assertEqual(Bookmark.objects.get(pk=2).title, 'localhost')

    def test_user_cannot_edit_another_bookmark(self):
        """
        An authenticated user should not be able to edit other's bookmarks.
        """
        self.client.force_login(user=User.objects.get(username='dummy'))
        response = self.client.get('/edit/3/')
        self.assertEqual(response.status_code, 403)

    def test_superuser_get_form_another_bookmark(self):
        """
        A superuser should be able to access the edit form for a
        bookmark belonging to any user.
        """
        self.client.force_login(user=User.objects.get(username='superuser'))
        response = self.client.get('/edit/1/')
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_edit_another_bookmark(self):
        """
        A superuser should be able to edit all bookmarks.
        """
        self.client.force_login(user=User.objects.get(username='superuser'))
        response = self.client.post(
            '/edit/1/',
            {
                'bookmark_url': 'http://localhost:8000',
                'title': 'localhost',
                'is_public': True,
                'tags': [1, 2, 3]
            }
        )
        self.assertRedirects(response, '/')
        self.assertEqual(Bookmark.objects.get(pk=1).title, 'localhost')


class BookmarkDeleteTestCase(TestCase):
    fixtures = ['bookmark', 'tag', 'user']

    def test_delete_is_protected(self):
        """
        An unauthenticated user should not be able to access the form.
        A redirect to the login page should follow up.
        """
        response = self.client.get('/delete/1/')
        self.assertRedirects(response, '/login/?next=/delete/1/')

    def test_user_get_delete_form(self):
        """
        An authenticated user should be able to access the delete form.
        """
        self.client.force_login(user=User.objects.get(username='dummy'))
        response = self.client.get('/delete/2/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_user_delete_own_bookmark(self):
        """
        An authenticated user should be able to delete own bookmarks.
        """
        self.client.force_login(user=User.objects.get(username='dummy'))
        response = self.client.post('/delete/2/')
        self.assertRedirects(response, '/')
        self.assertRaises(Bookmark.DoesNotExist, Bookmark.objects.get, pk=2)

    def test_user_cannot_delete_another_bookmark(self):
        """
        An authenticated user should not be able to delete other's bookmarks.
        """
        self.client.force_login(user=User.objects.get(username='dummy'))
        response = self.client.get('/edit/3/')
        self.assertEqual(response.status_code, 403)

    def test_superuser_get_form_another_bookmark(self):
        """
        A superuser should be able to access the delete form for a
        bookmark belonging to any user.
        """
        self.client.force_login(user=User.objects.get(username='superuser'))
        response = self.client.get('/edit/1/')
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_edit_another_bookmark(self):
        """
        A superuser should be able to delete bookmarks.
        """
        self.client.force_login(user=User.objects.get(username='superuser'))
        response = self.client.post('/delete/1/')
        self.assertRedirects(response, '/')
        self.assertRaises(Bookmark.DoesNotExist, Bookmark.objects.get, pk=1)
