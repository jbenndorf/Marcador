from rest_framework import serializers

from .models import Bookmark, Tag


class BookmarkSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'description', 'is_public', 'date_created', 'date_updated', 'owner', 'tags']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']
