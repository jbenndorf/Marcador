from django.contrib import admin

from .models import Bookmark, Tag


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('bookmark_url', 'title', 'owner', 'is_public', 'date_updated')
    list_editable = ('is_public',)
    list_filter = ('is_public', 'owner__username')
    search_fields = ['bookmark_url', 'title', 'description']
    readonly_fields = ('date_created', 'date_updated')


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Tag)