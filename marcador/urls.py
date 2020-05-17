from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'bookmarks', views.BookmarkViewSet)
router.register(r'tags', views.TagViewSet)


urlpatterns = [
    url(
        r'^user/(?P<username>[-\w]+)/$',
        views.bookmark_user,
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
        views.bookmark_list,
        name='marcador_bookmark_list'
    ),
    url(
        r'^api/',
        include(router.urls)

    ),
    url(
        r'^api-auth/',
        include('rest_framework.urls')
    )
]
