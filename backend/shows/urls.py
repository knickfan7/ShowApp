from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ShowsView, AuthenticatedShowsView


router = DefaultRouter()
router.register(r'shows', ShowsView, basename='shows')
router.register(r'add/show', AuthenticatedShowsView, basename='show')
urlpatterns = router.urls