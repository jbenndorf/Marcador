from marcador.models import Bookmark, Tag
from rest_framework import serializers

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bookmark
        fields=['url','title','description','is_public','date_created','date_updated','owner','tags']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=['name']
