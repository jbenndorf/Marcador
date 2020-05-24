from django.contrib.auth.models import User
from django.db.models import Prefetch, Q

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from marcador.models import Bookmark, Tag
from .filters import BookmarkFilter
from .permissions import (
    IsOwnerOrReadOnly,
    IsSuperuserOrReadOnly,
    IsPublicOrOwnerOrSuperuser
)
from .serializers import (
    BookmarkSerializer,
    NestedBookmarkSerializer,
    TagSerializer,
    UserSerializer
)


class TagViewSet(viewsets.ModelViewSet):
    """
    This **Tag View Set** automatically provides the following actions:

     - `list`
     - `create`
     - `retrieve`
     - `update` and `partial_update`
     - `destroy`

    Write operations are permitted only to superusers.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [
        IsSuperuserOrReadOnly
    ]


class BookmarkViewSet(viewsets.ModelViewSet):
    """
    This **Bookmark View Set** automatically provides
    the following actions:

    - `list`
    - `create`
    - `retrieve`

    `Update` and `destroy` operations are permitted
    only to owners of bookmarks or superusers.

    When filtering by __date created__ or __date updated__,
    please use the following ISO 8601 format:

    *YYYY-MM-DD hh:mm:ss*
    """
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        IsPublicOrOwnerOrSuperuser
    ]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = BookmarkFilter
    search_fields = ['title', 'bookmark_url', 'description']

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            bookmarks = Bookmark.public.all()
        elif self.request.user.is_superuser:
            bookmarks = self.queryset
        else:
            bookmarks = Bookmark.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True)
            )
        queryset = self.filter_queryset(bookmarks)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if not instance.is_public and instance.owner != request.user and not request.user.is_superuser:
    #         raise exceptions.PermissionDenied()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This **User View Set** automatically provides the following actions:

    - `list`
    - `retrieve`

    A custom `bookmarks` action can be performed on the user endpoints.
    """
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.prefetch_related(
                Prefetch(
                    'bookmarks',
                    Bookmark.public.all(),
                )
            )
        elif self.request.user.is_superuser:
            return self.queryset
        else:
            return self.queryset.prefetch_related(
                Prefetch(
                    'bookmarks',
                    Bookmark.objects.filter(
                        Q(owner=self.request.user) | Q(is_public=True)
                    )
                )
            )

    @action(detail=True)
    def bookmarks(self, request, *args, **kwargs):
        """An additional endpoint for listing all user's bookmarks."""
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
