from django.core.cache import cache
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
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
        # Cache the task list for the authenticated user
        user = self.request.user
        cache_key = f'task_list_{user.id}'
        cached_tasks = cache.get(cache_key)
        if cached_tasks is not None:
            return cached_tasks

        # If not cached, fetch from database and cache
        tasks = Task.objects.filter(assignee=user).select_related('assignee')
        cache.set(cache_key, tasks, timeout=60 * 15)
        return tasks

    def perform_create(self, serializer):
        instance = serializer.save()
        send_task_update_notification.delay(instance.id)
        cache.delete(f'task_list_{self.request.user.id}')

    def perform_update(self, serializer):
        instance = serializer.save()
        send_task_update_notification.delay(instance.id)
        cache.delete(f'task_list_{self.request.user.id}')

