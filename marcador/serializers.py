from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Bookmark, Tag


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.HyperlinkedRelatedField(
        view_name='tag-detail',
        queryset=Tag.objects.all(),
        many=True,
    )
    owner = serializers.CharField(read_only=True)
    date_created = serializers.DateTimeField(read_only=True)
    date_updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['url', 'id', 'bookmark_url', 'title', 'description', 'is_public',
                  'date_created', 'date_updated', 'owner', 'tags']


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ['url', 'id', 'name']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    bookmarks = BookmarkSerializer(many=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'bookmarks']
        extra_kwargs = {
            'url' : {'view_name': 'user-detail', 'lookup_field': 'username'},
        }
