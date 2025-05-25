from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import PlaylistViewSet

app_name = "uta"
urlpatterns = [
    path("", views.all_in_one, name="all_in_one"),
]

router = DefaultRouter()
router.register(r"playlists", PlaylistViewSet, basename="playlist")

urlpatterns += router.urls
