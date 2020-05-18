from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.db.models import Prefetch

from rest_framework import permissions
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response

from .forms import BookmarkForm
from .models import Bookmark, Tag
from .permissions import IsOwnerOrReadOnly, IsSuperuserOrReadOnly
from .serializers import BookmarkSerializer, TagSerializer, UserSerializer


def bookmark_list(request):
    bookmarks = Bookmark.public.all()
    if request.GET.get('tag'):
        bookmarks = bookmarks.filter(tags__name=request.GET['tag'])
    context = {'bookmarks': bookmarks}
    return render(request, 'marcador/bookmark_list.html', context)


def bookmark_user(request, username):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        bookmarks = user.bookmarks.all()
    else:
        bookmarks = Bookmark.public.filter(owner__username=username)
    if request.GET.get('tag'):
        bookmarks = bookmarks.filter(tags__name=request.GET['tag'])
    context = {'bookmarks': bookmarks, 'owner': user}
    return render(request, 'marcador/bookmark_user.html', context)


@login_required
def bookmark_create(request):
    if request.method == 'POST':
        form = BookmarkForm(data=request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.owner = request.user
            bookmark.save()
            form.save_m2m()
            return redirect('marcador_bookmark_user',
                username=request.user.username)
    else:
        form = BookmarkForm()
    context = {'form': form, 'create': True}
    return render(request, 'marcador/form.html', context)


@login_required
def bookmark_edit(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk)
    if bookmark.owner != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = BookmarkForm(instance=bookmark, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('marcador_bookmark_user',
                username=request.user.username)
    else:
        form = BookmarkForm(instance=bookmark)
    context = {'form': form, 'create': False}
    return render(request, 'marcador/form.html', context)


class DynamicSearchFilter(filters.SearchFilter):

    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])


# User can only UPDATE AND DELETE own bookmarks
class BookmarkViewSet(viewsets.ModelViewSet):
    """
    Bookmarks
    """
    queryset = Bookmark.public.all()
    serializer_class = BookmarkSerializer
    filter_backends = [DynamicSearchFilter]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get_queryset(self):
    #     result = Bookmark.objects.filter(owner=self.request.user) | Bookmark.objects.filter(is_public=True)
    #     return result


# Only supervisor can UPDATE AND DELETE bookmarks
class TagViewSet(viewsets.ModelViewSet):
    """
    Tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSuperuserOrReadOnly]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User
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

    # hier musst du den decorator einsetzen
    def bookmarks(self, request, *args, **kwargs):
        # hier sollst du eine variable bookmarks erstellen
        # und darin die bookmarks fuer den entsprechenden user
        # abfragen

        context = {
            'request': request
        }

        page = self.paginate_queryset(bookmarks)
        if page is not None:
            serializer = BookmarkSerializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = BookmarkSerializer(bookmarks, many=True, context=context)
        return Response(serializer.data)
