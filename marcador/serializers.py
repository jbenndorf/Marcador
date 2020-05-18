from rest_framework import serializers

from .models import Bookmark, Tag


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.HyperlinkedRelatedField(
        view_name='tag-detail',
        queryset=Tag.objects.all(),
        many=True,
    )
    owner = serializers.CharField(source='bookmark.owner', read_only=True)
    date_created = serializers.DateTimeField(read_only=True)
    date_updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['url', 'id', 'bookmark_url', 'title', 'description', 'is_public',
                  'date_created', 'date_updated', 'owner', 'tags']


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']
