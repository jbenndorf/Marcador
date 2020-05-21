from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from django_filters.views import FilterView

from marcador_api.filters import BookmarkFilter
from .models import Bookmark


class BookmarkList(FilterView):
    model = Bookmark
    context_object_name = 'bookmarks'
    template_name = 'marcador/bookmark_list.html'
    filterset_class = BookmarkFilter

    def get_queryset(self):
        bookmarks = Bookmark.public.all()
        return bookmarks


class UserBookmarkList(FilterView):
    context_object_name = 'bookmarks'
    template_name = 'marcador/bookmark_user.html'
    filterset_class = BookmarkFilter

    def __init__(self):
        self.user = User.objects.none()
        super(UserBookmarkList, self).__init__()

    def get_queryset(self):
        username = self.kwargs['username']
        self.user = get_object_or_404(User, username=username)
        if self.request.user == self.user:
            bookmarks = self.user.bookmarks.all()
        else:
            bookmarks = Bookmark.public.filter(owner__username=username)
        return bookmarks

    def get_context_data(self, **kwargs):
        context = super(UserBookmarkList, self).get_context_data(**kwargs)
        context['owner'] = self.user
        return context


class BookmarkCreate(LoginRequiredMixin, CreateView):
    model = Bookmark
    fields = ['bookmark_url', 'title', 'description', 'is_public', 'tags']
    success_url = reverse_lazy('bookmark-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(BookmarkCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BookmarkCreate, self).get_context_data(**kwargs)
        context['create'] = True
        return context


class BookmarkUpdate(LoginRequiredMixin, UpdateView):
    model = Bookmark
    fields = ['bookmark_url', 'title', 'description', 'is_public', 'tags']
    success_url = reverse_lazy('bookmark-list')

    def get_context_data(self, **kwargs):
        context = super(BookmarkUpdate, self).get_context_data(**kwargs)
        context['create'] = False
        return context


class BookmarkDelete(LoginRequiredMixin, DeleteView):
    model = Bookmark
    context_object_name = 'bookmark'
    success_url = reverse_lazy('bookmark-list')
