from django.urls import path
from .views import UserCreateView, UserProfileView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]