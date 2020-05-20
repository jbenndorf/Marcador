from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'bookmarks', views.BookmarkViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url('^', include(router.urls)),
]
