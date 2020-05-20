from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.BookmarkList.as_view(),
        name='bookmark-list',
    ),
    url(
        r'^user/(?P<username>[-\w]+)/$',
        views.UserBookmarkList.as_view(),
        name='bookmark-user',
    ),
    url(
        r'^create/$',
        views.BookmarkCreate.as_view(),
        name='bookmark-create',
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        views.BookmarkUpdate.as_view(),
        name='bookmark-edit',
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        views.BookmarkDelete.as_view(),
        name='bookmark-delete',
    )
]
