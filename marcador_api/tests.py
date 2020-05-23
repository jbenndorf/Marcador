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

    def test_not_authenticated_can_read_tags(self):
        """
        Not authenticated users should be able to perform the list
        action on the endpoint tags.
        """
        response = self.client.get(reverse(self.list_view))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_not_authenticated_can_read_a_tag(self):
        """
        Not authenticated users should be able to perform the retrieve
        action on the endpoint tags.
        """
        response = self.client.get(reverse(self.detail_view, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')

    def test_not_authenticated_cannot_create_tags(self):
        """
        Not authenticated users should not be able to perform the
        create action on the endpoint tags.
        """
        response = self.client.post(
            reverse(self.list_view),
            {'name': 'create'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_cannot_update_a_tag(self):
        """
        Not authenticated users should not be able to perform the
        update action on the endpoint tags.
        """
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'name': 'update'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_cannot_delete_a_tag(self):
        """
        Not authenticated users should not be able to perform the
        destroy action on the endpoint tags.
        """
        response = self.client.post(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'name': 'delete'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_can_read_tags(self):
        """
        Authenticated users should be able to perform the list action
        on the endpoint tags.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(reverse(self.list_view))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_authenticated_can_read_a_tag(self):
        """
        Authenticated users should be able to perform the retrieve action
        on the endpoint tags.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(reverse(self.detail_view, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')

    def test_authenticated_cannot_create_tags(self):
        """
        Authenticated users should not be able to perform the create
        action on the endpoint tags.
        """
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse(self.list_view),
            {'name': 'create'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_cannot_update_a_tag(self):
        """
        Authenticated users should not be able to perform the update
        action on the endpoint tags.
        """
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse(self.list_view),
            {'name': 'update'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_cannot_delete_a_tag(self):
        """
        Authenticated users should not be able to perform the delete
        action on the endpoint tags.
        """
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse(self.list_view),
            {'name': 'delete'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_read_tags(self):
        """
        Superusers should be able to perform the list action on the
        endpoint tags.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(reverse(self.list_view))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_superuser_can_read_a_tags(self):
        """
        Superusers should be able to perform the retrieve action on the
        endpoint tags.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(reverse(self.detail_view, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')

    def test_superuser_can_create_tags(self):
        """
        Superusers should be able to perform the create action on the
        endpoint tags.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.post(
            reverse(self.list_view),
            {'name': 'create'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_update_a_tag(self):
        """
        Superusers should be able to perform the update action on the
        endpoint tags.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'name': 'update'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'update')

    def test_superuser_can_delete_a_tag(self):
        """
        Superusers should be able to perform the delete action on the
        endpoint tags.
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

    def test_not_authenticated_can_read_public_bookmarks(self):
        """
        Not authenticated users should be able to perform the list
        action on the endpoint bookmarks. They should be able to read
        only the public bookmarks.
        """
        response = self.client.get(reverse(self.list_view))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_not_authenticated_can_read_a_public_bookmark(self):
        """
        Not authenticated users should be able to perform the retrieve
        action on the endpoints bookmarks. They should be able to read
        a public bookmark.
        """
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'example')

    def test_not_authenticated_cannot_read_a_private_bookmark(self):
        """
        Not authenticated users should not be able to read a private
        bookmark.
        """
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_cannot_create_bookmarks(self):
        """
        Not authenticated users should not be able to perform the
        create action on the endpoint bookmarks.
        """
        response = self.client.post(
            reverse(self.list_view),
            {'bookmark_url': 'https://www.test.com/', 'title': 'Test'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_cannot_update_a_bookmark(self):
        """
        Not authenticated users should not be able to perform the
        update action on the endpint bookmarks.
        """
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'bookmark_url': 'https://www.example.com/', 'title': 'Example'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_cannot_delete_a_bookmark(self):
        """
        Not authenticated users should not be able to perform the
        destroy action on the endpoint bookmarks.
        """
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'name': 'delete'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_can_read_public_bookmarks_and_own_bookmarks(self):
        """
        Authenticated users should be able to perform the list action
        on the endpoint bookmarks. They should be able to read all
        public bookmarks and all own bookmarks.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.get(reverse(self.list_view))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_authenticated_can_read_an_own_private_bookmark(self):
        """
        Authenticated users should be able to perform the retrieve
        action on the endpoint bookmarks. They should be able to read
        an own private bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'example uk')

    def test_authenticated_cannot_read_a_foreign_private_bookmark(self):
        """
        Authenticated users should not be able to read someone else's
        private bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 4})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_can_create_bookmarks(self):
        """
        Authenticated users should be able to perform the create action
        on the endpoint bookmarks.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.post(
            reverse(self.list_view),
            {'bookmark_url': 'https://www.test.com/', 'title': 'Test'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_can_update_an_own_public_bookmark(self):
        """
        Authenticated users should be able to perform the update action
        on the endpoint bookmarks. They should be able to update an own
        public bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'bookmark_url': 'https://www.example.com/', 'title': 'Example'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bookmark_url'], 'https://www.example.com/')
        self.assertEqual(response.data['title'], 'Example')

    def test_authenticated_can_update_an_own_private_bookmark(self):
        """
        Authenticated users should be able to update an own private
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

    def test_authenticated_cannot_edit_a_foreign_bookmark(self):
        """
        Authenticated users should not be able to update a foreign
        bookmark.
        """
        self.client.force_login(user=self.user_b)
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'bookmark_url': 'https://www.example.com/', 'title': 'Example'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_can_delete_an_own_public_bookmark(self):
        """
        Authenticated users should be able to perform the destroy
        action on the endpoint bookmarks. They should be able to
        delete an own public bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.delete(
            reverse(self.detail_view, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_can_delete_an_own_private_bookmark(self):
        """
        Authenticated users should be able to delete an own private
        bookmark.
        """
        self.client.force_login(user=self.user_a)
        response = self.client.delete(
            reverse(self.detail_view, kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_cannot_delete_a_foreign_bookmark(self):
        """
        Authenticated user should not be able to delete a foreign
        bookmark.
        """
        self.client.force_login(user=self.user_b)
        response = self.client.delete(
            reverse(self.detail_view, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_read_bookmarks(self):
        """
        Superusers should be able to perform the list action on the
        endpoint bookmarks. They should be able to read all bookmarks,
        both public and private from all users.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(reverse(self.list_view))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_superuser_can_read_a_public_bookmark(self):
        """
        Superusers should be able to perform the retrieve action on the
        endpoint bookmarks. They should be able to ready a public
        bookmark belonging to any user.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((response.data['title']), 'example')

    def test_superuser_can_read_a_private_bookmark(self):
        """
        Superusers should be able to read a private bookmarks belonging
        to any user.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(
            reverse(self.detail_view, kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((response.data['title']), 'example uk')

    def test_superuser_can_create_bookmarks(self):
        """
        Superusers should be able to perform the create action on the
        endpoint bookmarks.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.post(
            reverse(self.list_view),
            {'bookmark_url': 'https://www.test.com/', 'title': 'Test'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_update_a_public_bookmark(self):
        """
        Superusers should be able to perform the update action on the
        endpoint bookmarks. They should be able to update a public
        bookmark belonging to any user.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 1}),
            {'bookmark_url': 'https://www.example.com/', 'title': 'Example'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bookmark_url'], 'https://www.example.com/')
        self.assertEqual(response.data['title'], 'Example')

    def test_superuser_can_update_a_private_bookmark(self):
        """
        Superusers should be able to update a private
        bookmark belonging to any user.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.put(
            reverse(self.detail_view, kwargs={'pk': 2}),
            {'bookmark_url': 'https://www.example.com/', 'title': 'Example'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bookmark_url'], 'https://www.example.com/')
        self.assertEqual(response.data['title'], 'Example')

    def test_superuser_can_delete_a_public_bookmark(self):
        """
        Superusers should be able to perform the destroy action on the
        endpoint bookmarks. They should be able to delete a public
        bookmark belonging to any user.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.delete(
            reverse(self.detail_view, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_can_delete_private_bookmark(self):
        """
        Superusers should be able to delete a private bookmark
        belonging to any user.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.delete(
            reverse(self.detail_view, kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_bookmarks_using_searchfilter(self):
        """
        All users should be able to filter the bookmarks by a search
        term that occurs inside the URL, title or description of the
        bookmark.
        """
        response = self.client.get(
            f'{reverse(self.list_view)}?search=just'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_bookmarks_by_tag(self):
        """
        All users should be able to filter the bookmarks by a given
        tag.
        """
        tag = Tag.objects.get(pk=1)
        response = self.client.get(
            f'{reverse(self.list_view)}?tags={tag.name}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class UserViewSetTestCase(APITestCase):
    list_view = 'marcador_api:user-list'
    detail_view = 'marcador_api:user-detail'
    bookmarks_view = 'marcador_api:user-bookmarks'

    def setUp(self):
        self.user = User.objects.create(username='test', password='testpass')
        self.superuser = User.objects.create(
            username='admin',
            password='adminpass',
            is_superuser=True,
        )
        self.test_tag = Tag.objects.create(name='test')
        self.public = Bookmark.objects.create(
            bookmark_url='http://example.com/',
            title='example',
            description='This is just an example',
            owner=self.user,
        )
        self.public.tags.add(self.test_tag)
        self.private = Bookmark.objects.create(
            bookmark_url='http://example.co.uk/',
            title='example uk',
            is_public=False,
            owner=self.user,
        )
        self.private.tags.add(self.test_tag)

    def test_user_can_read_users(self):
        """
        All user should be able to perform the list action on the
        endpoint users.
        """
        response = self.client.get(reverse(self.list_view))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_user_can_read_a_user(self):
        """
        All users should be able to perform the retrieve action on the
        endpoint users.
        """
        response = self.client.get(
            reverse(self.detail_view, kwargs={'username': 'test'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'test')
        self.assertEqual(len(response.data['bookmarks']), 1)
        self.assertEqual(response.data['bookmarks'][0]['title'], 'example')

    def test_user_can_read_own_entry_with_all_bookmarks(self):
        """
        All users should be able to read their own entry with all
        bookmarks.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse(self.detail_view, kwargs={'username': 'test'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'test')
        self.assertEqual(len(response.data['bookmarks']), 2)
        self.assertEqual(response.data['bookmarks'][0]['title'], 'example uk')
        self.assertEqual(response.data['bookmarks'][1]['title'], 'example')

    def test_user_can_read_users_public_bookmarks(self):
        """
        All users should be able to perform the custom bookmarks action
        on the endpoint users. They should be able to read only the
        public bookmarks of another user.
        """
        response = self.client.get(
            reverse(self.bookmarks_view, kwargs={'username': 'test'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'example')

    def test_user_can_read_own_bookmarks(self):
        """
        All users should be able to read all of their bookmarks.
        """
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse(self.bookmarks_view, kwargs={'username': 'test'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'example uk')
        self.assertEqual(response.data[1]['title'], 'example')

    def test_superuser_can_read_all_bookmarks(self):
        """
        Superusers should be able to perform the custom bookmark action
        on the endpoint users. They should be able to read all
        bookmarks.
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(
            reverse(self.bookmarks_view, kwargs={'username': 'test'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'example uk')
        self.assertEqual(response.data[1]['title'], 'example')
