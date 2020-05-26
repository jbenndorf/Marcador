from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .apps import MarcadorApiConfig
from . import views

router = DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'bookmarks', views.BookmarkViewSet)
router.register(r'users', views.UserViewSet)

app_name = MarcadorApiConfig.name
urlpatterns = [
    url('^', include(router.urls)),
]
