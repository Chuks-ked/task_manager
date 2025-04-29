from django.core.cache import cache
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer
from .tasks import send_task_update_notification
from .permissions import IsAssigneeOrReadOnly

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAssigneeOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user).select_related('assignee')

    def list(self, request, *args, **kwargs):
        user = self.request.user
        cache_key = f'task_list_{user.id}'
        cached_tasks = cache.get(cache_key)

        if cached_tasks is not None:
            # Cached data is already serialized, return it directly in a Response
            return Response(cached_tasks)

        # Fetch tasks from the database
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        task_data = serializer.data
        cache.set(cache_key, task_data, timeout=60 * 15)
        return Response(task_data)

    def perform_create(self, serializer):
        instance = serializer.save()
        send_task_update_notification.delay(instance.id)
        cache.delete(f'task_list_{self.request.user.id}')
        # Invalidate FastAPI caches
        cache.delete(f'public_task_{instance.id}')
        cache.delete(f'task_status_{instance.id}')

    def perform_update(self, serializer):
        instance = serializer.save()
        send_task_update_notification.delay(instance.id)
        cache.delete(f'task_list_{self.request.user.id}')
        # Invalidate FastAPI caches
        cache.delete(f'public_task_{instance.id}')
        cache.delete(f'task_status_{instance.id}')


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        self.perform_destroy(instance)
        cache.delete(f'task_list_{user.id}')
        # Invalidate public endpoint caches
        cache.delete(f'public_task_{instance.id}')
        cache.delete(f'task_status_{instance.id}')
        return Response(status=status.HTTP_204_NO_CONTENT)

