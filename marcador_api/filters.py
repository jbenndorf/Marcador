from django_filters import rest_framework as filters

from marcador.models import Bookmark, Tag


class BookmarkFilter(filters.FilterSet):
    date_created = filters.IsoDateTimeFromToRangeFilter(field_name='date_created')
    date_updated = filters.IsoDateTimeFromToRangeFilter(field_name='date_updated')
    tags = filters.ModelChoiceFilter(field_name='tags', to_field_name='name', queryset=Tag.objects.all())

    class Meta:
        model = Bookmark
        fields = ['date_created', 'date_updated', 'tags']
