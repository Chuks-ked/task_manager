# from django.contrib import admin
# from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework.routers import DefaultRouter
# from task_manager.fastapi_app import app as fastapi_app
# from fastapi.middleware.wsgi import WSGIMiddleware
# from core.views import UserCreateView, UserProfileView, TaskViewSet

# router = DefaultRouter()
# router.register(r'tasks', TaskViewSet)

# fastapi_mount =WSGIMiddleware(fastapi_app)

# urlpatterns = [
#     # path('api/public/', fastapi_mount, name='fastapi'),
#     path('admin/', admin.site.urls),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/', include('core.urls')),
#     path('api/', include(router.urls)),
    
# ]

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from core.views import UserCreateView, UserProfileView, TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('core.urls')),
    path('api/', include(router.urls)),
]