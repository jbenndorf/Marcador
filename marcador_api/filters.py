from django_filters import rest_framework as filters

from marcador.models import Bookmark, Tag


class BookmarkFilter(filters.FilterSet):
    date_created = filters.IsoDateTimeFromToRangeFilter()
    date_updated = filters.IsoDateTimeFromToRangeFilter()
    tags = filters.ModelChoiceFilter(
        queryset=Tag.objects.all(),
        to_field_name='name',
    )

    class Meta:
        model = Bookmark
        fields = ['date_created', 'date_updated', 'tags']
