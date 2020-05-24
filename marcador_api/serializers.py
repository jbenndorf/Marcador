from django.contrib.auth.models import User

from rest_framework import serializers

from marcador.models import Bookmark, Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'id', 'name']
        extra_kwargs = {
            'url': {'view_name': 'marcador_api:tag-detail'}
        }


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['url', 'id', 'bookmark_url', 'title', 'description',
                  'is_public', 'date_created', 'date_updated', 'owner', 'tags']
        extra_kwargs = {
            'url': {'view_name': 'marcador_api:bookmark-detail'},
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            'owner': {
                'view_name': 'marcador_api:user-detail',
                'lookup_field': 'username',
                'read_only': True
            },
            'tags': {
                'view_name': 'marcador_api:tag-detail',
                'queryset': Tag.objects.all(),
                'many': True
            },
        }


class NestedBookmarkSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Bookmark
        fields = ['url', 'id', 'bookmark_url', 'title', 'description',
                  'is_public', 'date_created', 'date_updated', 'tags']
        extra_kwargs = {
            'url': {'view_name': 'marcador_api:bookmark-detail'}
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    bookmarks = NestedBookmarkSerializer(many=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'bookmarks']
        extra_kwargs = {
            'url': {
                'view_name': 'marcador_api:user-detail',
                'lookup_field': 'username'
            },
        }
