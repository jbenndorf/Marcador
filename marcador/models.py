# encoding: utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

__all__ = ('Tag', 'Bookmark')


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ['name']

    def __str__(self):
        return self.name


class BookmarkQuerySet(models.QuerySet):
    def with_owner(self):
        return self.select_related('owner')

    def with_tags(self):
        return self.prefetch_related('tags')

    def public(self):
        return self.filter(is_public=True)

    def with_related(self):
        return self.with_owner().with_tags()


class PublicBookmarkManager(models.Manager):
    def get_queryset(self):
        qs = super(PublicBookmarkManager, self).get_queryset()
        return qs.filter(is_public=True)


class Bookmark(models.Model):
    bookmark_url = models.URLField('URL')
    title = models.CharField('title', max_length=255)
    description = models.TextField('description', blank=True)
    is_public = models.BooleanField('public', default=True)
    date_created = models.DateTimeField('date created')
    date_updated = models.DateTimeField('date updated')
    owner = models.ForeignKey(
        User, verbose_name='owner',
        related_name='bookmarks'
    )
    tags = models.ManyToManyField(Tag, blank=True)

    objects = BookmarkQuerySet.as_manager()
    public = PublicBookmarkManager()

    class Meta:
        verbose_name = 'bookmark'
        verbose_name_plural = 'bookmarks'
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.title} ({self.bookmark_url})'

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = now()
        self.date_updated = now()
        super(Bookmark, self).save(*args, **kwargs)
