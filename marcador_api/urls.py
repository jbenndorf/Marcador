from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from marcador_api import views

router = DefaultRouter()
router.register(r'bookmarks', views.BookmarkViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'users', views.UserViewSet)

app_name = 'marcador_api'
urlpatterns = [
    url('^', include(router.urls)),
]