from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'bookmarks', views.BookmarkViewSet)
router.register(r'users', views.UserViewSet)

app_name = 'marcador_api'
urlpatterns = [
    url('^', include(router.urls)),
]
