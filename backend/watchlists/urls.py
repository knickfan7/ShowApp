from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WatchlistView


router = DefaultRouter()
router.register(r'watchlists', WatchlistView, basename='Watchlists')
urlpatterns = router.urls