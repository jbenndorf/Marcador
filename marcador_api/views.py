from django.contrib.auth.models import User
from django.db.models import Prefetch

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from marcador.models import Bookmark, Tag
from .filters import BookmarkFilter
from .permissions import IsOwnerOrReadOnly, IsSuperuserOrReadOnly
from .serializers import (
    BookmarkSerializer,
    NestedBookmarkSerializer,
    TagSerializer,
    UserSerializer
)


class TagViewSet(viewsets.ModelViewSet):
    """
    This Tag View Set automatically provides 'list', 'create' and 'retrieve'
    actions for authenticated users.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperuserOrReadOnly
    ]


class BookmarkViewSet(viewsets.ModelViewSet):
    """
    This Bookmark View Set automatically provides 'list', 'create' and 'retrieve'
    actions for authenticated users. Owners of bookmarks can perform 'update' and 'delete' actions.

    When filtering by 'date created' or 'date updated', please use the following format:
    """
    queryset = Bookmark.public.all()
    serializer_class = BookmarkSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = BookmarkFilter
    search_fields = ['title', 'bookmark_url', 'description']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This User View Set automatically provides 'list' and 'retrieve' actions.

    User instances are accessible by username.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return self.queryset.prefetch_related(
            Prefetch(
                'bookmarks',
                Bookmark.public.all(),
            )
        )

    @action(detail=True)
    def bookmarks(self, request, *args, **kwargs):
        """An additional endpoint for listing all user's bookmarks"""
        user = self.get_object()
        bookmarks = Bookmark.public.filter(owner=user)
        if request.user.is_authenticated and (request.user == user or
                                              request.user.is_superuser):
            bookmarks = Bookmark.objects.filter(owner=user)

        context = {
            'request': request
        }

        page = self.paginate_queryset(bookmarks)
        if page is not None:
            serializer = NestedBookmarkSerializer(
                page,
                many=True,
                context=context
            )
            return self.get_paginated_response(serializer.data)

        serializer = NestedBookmarkSerializer(
            bookmarks,
            many=True,
            context=context
        )
        return Response(serializer.data)
