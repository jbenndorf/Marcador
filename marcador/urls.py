from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^user/(?P<username>[-\w]+)/$',
        views.UserBookmarkList.as_view(),
        name='marcador_bookmark_user'
    ),
    url(
        r'^create/$',
        views.bookmark_create,
        name='marcador_bookmark_create'
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        views.bookmark_edit,
        name='marcador_bookmark_edit'
    ),
    url(
        r'^$',
        views.BookmarkList.as_view(),
        name='bookmark-list'
    ),
]
