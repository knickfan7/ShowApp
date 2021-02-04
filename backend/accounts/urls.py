from django.urls import path, include
from knox.views import LogoutView

from .views import LoginAPIView, RegisterAPIView, UserAPIView

urlpatterns = [
    path('', include('knox.urls')),
    path('user/', UserAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('logins/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view(), name='knox_logout')
]
