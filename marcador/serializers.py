from rest_framework import serializers

from .models import Bookmark, Tag


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.HyperlinkedRelatedField(many=True, view_name='tag-detail', read_only=True)
    owner = serializers.StringRelatedField(source='owner.username')

    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'description', 'is_public', 'date_created', 'date_updated', 'owner', 'tags']


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']
