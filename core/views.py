from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer
from .tasks import send_task_update_notification

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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        send_task_update_notification.delay(instance.id)

    def perform_update(self, serializer):
        instance = serializer.save()
        send_task_update_notification.delay(instance.id)