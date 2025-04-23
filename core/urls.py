from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserCreateView, UserProfileView, TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]