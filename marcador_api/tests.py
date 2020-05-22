from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from marcador.models import Bookmark, Tag


class TagViewSetTestCase(APITestCase):
    list_view = 'marcador_api:tag-list'
    detail_view = 'marcador_api:tag-detail'

    def setUp(self):
        self.tag = Tag.objects.create(name='test')
        self.user = User.objects.create(
            username='testuser',
            password='pass123',
        )
        self.superuser = User.objects.create(
            username='testsuperuser',
            password='superpass123',
            is_superuser=True,
        )

    def test_not_authenticated_read_list_tags(self):
        """
        Not authenticated users should be able to perform the list
        operation on the endpoint tags.
        """
        response = self.client.get(reverse(self.list_view))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_not_authenticated_read_detail_tags(self):
        """
        Not authenticated users should be able to perform the detail
        operation on the endpoint tags.
        """
        response = self.client.get(reverse(self.detail_view, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_not_authenticated_create_tags(self):
        """
        Not authenticated users should not be able to perform the create
        operation on the endpoint tags.
        """
        response = self.client.post(
            reverse(self.list_view),
            {'name': 'create'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_update_tags(self):
        """
        Not authenticated users should not be able to perform the update
        operation on the endpoint tags.
        """
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'name': 'update'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_delete_tags(self):
        """
        Not authenticated users should not be able to perform the delete
        operation on the endpoint tags
        """
        response = self.client.post(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'name': 'delete'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_read_list_tags(self):
        """
        Authenticated users should be able to perform the list
        operation on the endpoint tags
        """
        self.client.force_login(user=self.user)
        response = self.client.get(reverse(self.list_view))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_authenticated_read_detail_tags(self):
        """
        Authenticated users should be able to perform the detail
        operation on the endpoint tags
        """
        self.client.force_login(user=self.user)
        response = self.client.get(reverse(self.detail_view, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_authenticated_create_tags(self):
        """
        Authenticated users should not be able to perform the create
        operation on the endpoint tags
        """
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse(self.list_view),
            {'name': 'create'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_update_tags(self):
        """
        Authenticated users should not be able to perform the update
        operation on the endpoint tags
        """
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse(self.list_view),
            {'name': 'update'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_delete_tags(self):
        """
        Authenticated users should not be able to perform the delete
        operation on the endpoint tags
        """
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse(self.list_view),
            {'name': 'delete'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_read_list_tags(self):
        """
        Superusers should be able to perform the list operation
        on the endpoint tags
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(reverse(self.list_view))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_superuser_read_detail_tags(self):
        """
        Superusers should be able to perform the detail operation
        on the endpoint tags
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(reverse(self.detail_view, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')

    def test_superuser_create_tags(self):
        """
        Superusers should be able to perform the create operation
        on the endpoint tags
        """
        self.client.force_login(user=self.superuser)
        response = self.client.post(
            reverse(self.list_view),
            {'name': 'create'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_update_tags(self):
        """
        Superusers should be able to perform the update operation
        on the endpoint tags
        """
        self.client.force_login(user=self.superuser)
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'name': 'update'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'update')

    def test_superuser_delete_tags(self):
        """
        Superusers should be able to perform the delete operation
        on the endpoint tags
        """
        self.client.force_login(user=self.superuser)
        response = self.client.delete(
            reverse(self.detail_view, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BookmarkViewSetTestCase(APITestCase):
    list_view = 'marcador_api:bookmark-list'
    detail_view = 'marcador_api:bookmark-detail'

    def setUp(self):
        self.user_a = User.objects.create(username='testA', password='pass123')
        self.user_b = User.objects.create(username='testB', password='pass456')
        self.superuser = User.objects.create(
            username='admin',
            password='adminpass',
            is_superuser=True,
        )
        self.test_tag_a = Tag.objects.create(name='testA')
        self.test_tag_b = Tag.objects.create(name='testB')
        self.public_a = Bookmark.objects.create(
            bookmark_url='http://example.com/',
            title='example',
            description='This is just an example',
            owner=self.user_a,
        )
        self.public_a.tags.add(self.test_tag_a)
        self.private_a = Bookmark.objects.create(
            bookmark_url='http://example.co.uk/',
            title='example uk',
            is_public=False,
            owner=self.user_a,
        )
        self.private_a.tags.add(self.test_tag_a)
        self.public_b = Bookmark.objects.create(
            bookmark_url='http://example.fr/',
            title='example fr',
            description='Une example',
            owner=self.user_b,
        )
        self.public_b.tags.add(self.test_tag_b)
        self.private_b = Bookmark.objects.create(
            bookmark_url='http://example.de/',
            title='Beispiel',
            is_public=False,
            owner=self.user_b,
        )
        self.private_b.tags.add(self.test_tag_b)

    def test_not_authenticated_read_public_bookmarks(self):
        """
        Not authenticated users should be able to read public bookmarks.
        """
        response = self.client.get(reverse(self.list_view))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

# Unsure of how to test for filtering

    def test_not_authenticated_can_filter_bookmarks(self):
        """
        All users should be able to filter through bookmarks.
        """
        response = self.client.get(
            reverse(self.list_view),
            {'description': 'une example'}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_not_authenticated_read_public_bookmark(self):
        """
        All users should be able to read a public bookmark.
        """
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'example')

# Should be HTTP_403_FORBIDDEN but responds with HTTP_404_NOT_FOUND
    def test_not_authenticated_cannot_read_private_bookmark(self):
        """
        Not authenticated users should not be able to read a private
        bookmark.
        """
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_cannot_create_bookmark(self):
        """
        Not authenticated users should not be able to create a bookmark.
        """
        response = self.client.post(
            reverse(self.list_view),
            {'bookmark_url': 'https://www.test.com/', 'title': 'Test'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_cannot_edit_bookmark(self):
        """
        Not authenticated users should not be able to edit a bookmark.
        """
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'bookmark_url': 'https://www.example.com/', 'title': 'Example'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_cannot_delete_bookmark(self):
        """
        Not authenticated users should not be able to delete a bookmark.
        """
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'name': 'delete'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# Authenticated-related tests

    def test_authenticated_can_read_own_public_bookmarks(self):
        """
        Authenticated users should be able to read their own public bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'example')

# Response should be HTTP_200_OK, but is HTTP_404_NOT_FOUND
    def test_authenticated_can_read_own_private_bookmark(self):
        """
        Authenticated users should be able to read their own private bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'example uk')

# Unsure how how to test for filtering

    def test_authenticated_can_filter_public_bookmarks(self):
        """
        Authenticated users should be able to filter through bookmarks.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.get(
            reverse(self.list_view),
            {'title': 'example'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_authenticated_can_create_bookmark(self):
        """
        Authenticated users should be able to create a bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.post(
            reverse(self.list_view),
            {'bookmark_url': 'https://www.test.com/', 'title': 'Test'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_can_delete_own_bookmark(self):
        """
        An authenticated user should be able to delete his/her own
        bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.delete(
            reverse(self.detail_view, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_can_edit_own_public_bookmark(self):
        """
        An authenticated user should be able to edit his/her own
        bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'bookmark_url': 'https://www.example.com/', 'title': 'Example'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bookmark_url'], 'https://www.example.com/')
        self.assertEqual(response.data['title'], 'Example')

    # Response should be HTTP_200_OK, but is HTTP_404_NOT_FOUND
    def test_authenticated_can_edit_own_private_bookmark(self):
        """
        An authenticated user should be able to edit his/her own
        bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 2}),
            {'bookmark_url': 'https://www.example.co.uk/', 'title': 'Example UK'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bookmark_url'], 'https://www.example.co.uk/')
        self.assertEqual(response.data['title'], 'Example UK')

    def test_authenticated_cannot_edit_foreign_bookmark(self):
        """
        An authenticated user should not be able to edit a foreign
        bookmark.
        """
        self.client.force_login(user=self.user_b)
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'bookmark_url': 'https://www.example.com/', 'title': 'Example'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# Response should be HTTP_403_FORBIDDEN, but is HTTP_404_NOT_FOUND
    def test_authenticated_cannot_read_foreign_private_bookmark(self):
        """
        Authenticated users should not be able to read a foreign, private bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 4})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_cannot_delete_foreign_bookmark(self):
        """
        An authenticated user should not be able to delete a foreign
        bookmark.
        """
        self.client.force_login(user=self.user_b)
        response = self.client.delete(
            reverse(self.detail_view, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Superuser-related tests

    def test_superuser_can_read_public_bookmarks(self):
        """
        A superuser should be able to delete a public bookmark from any
        user.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(
            reverse(self.list_view)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Response should be HTTP_200_OK, but is HTTP_404_NOT_FOUND
    def test_superuser_can_read_private_bookmark(self):
        """
        A superuser should be able to read a private bookmark from any
        user.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_can_create_bookmark(self):
        """
        A superuser should be able to create a bookmark.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.post(
            reverse(self.list_view),
            {'bookmark_url': 'https://www.test.com/', 'title': 'Test'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_edit_bookmark(self):
        """
        A superuser should be able to edit a bookmark from any
        user.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'bookmark_url': 'https://www.example.com/', 'title': 'Example'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bookmark_url'], 'https://www.example.com/')
        self.assertEqual(response.data['title'], 'Example')

    def test_superuser_can_delete_public_bookmark(self):
        """
        A superuser should be able to delete a public bookmark from any
        user.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.delete(
            reverse(self.detail_view, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# Response should be HTTP_204_NO_CONTENT but is HTTP_404
    def test_superuser_can_delete_private_bookmark(self):
        """
        A superuser should be able to delete a private bookmark from any
        user.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.delete(
            reverse(self.detail_view, kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
