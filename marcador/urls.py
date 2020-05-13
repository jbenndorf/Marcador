from django.conf.urls import url

from . import views

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
]
