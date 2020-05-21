from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from marcador.models import Bookmark, Tag


class TagViewSetTestCase(APITestCase):
    list = 'marcador_api:tag-list'
    detail = 'marcador_api:tag-detail'

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
        response = self.client.get(reverse(self.list))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_not_authenticated_read_detail_tags(self):
        """
        Not authenticated users should be able to perform the detail
        operation on the endpoint tags.
        """
        response = self.client.get(reverse(self.detail, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_not_authenticated_create_tags(self):
        """
        Not authenticated users should not be able to perform the create
        operation on the endpoint tags
        """
        response = self.client.post(
            reverse(self.list),
            {'name': 'create'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_update_tags(self):
        """
        Not authenticated users should not be able to perform the update
        operation on the endpoint tags
        """
        response = self.client.put(
            reverse(self.detail, kwargs={'pk': 1}),
            {'name': 'update'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated_delete_tags(self):
        """
        Not authenticated users should not be able to perform the delete
        operation on the endpoint tags
        """
        response = self.client.post(
            reverse(self.detail, kwargs={'pk': 1}),
            {'name': 'delete'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_read_list_tags(self):
        """
        Authenticated users should be able to perform the list
        operation on the endpoint tags
        """
        self.client.force_login(user=self.user)
        response = self.client.get(reverse(self.list))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_authenticated_read_detail_tags(self):
        """
        Authenticated users should be able to perform the detail
        operation on the endpoint tags
        """
        self.client.force_login(user=self.user)
        response = self.client.get(reverse(self.detail, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_authenticated_create_tags(self):
        """
        Authenticated users should not be able to perform the create
        operation on the endpoint tags
        """
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse(self.list),
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
            reverse(self.list),
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
            reverse(self.list),
            {'name': 'delete'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_read_list_tags(self):
        """
        Superusers should be able to perform the list operation
        on the endpoint tags
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(reverse(self.list))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_superuser_read_detail_tags(self):
        """
        Superusers should be able to perform the detail operation
        on the endpoint tags
        """
        self.client.force_login(user=self.superuser)
        response = self.client.get(reverse(self.detail, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')

    def test_superuser_create_tags(self):
        """
        Superusers should be able to perform the create operation
        on the endpoint tags
        """
        self.client.force_login(user=self.superuser)
        response = self.client.post(
            reverse(self.list),
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
            reverse(self.detail, kwargs={'pk': 1}),
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
            reverse(self.detail, kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
