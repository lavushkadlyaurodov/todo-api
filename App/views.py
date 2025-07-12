from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Task, TaskPermission
from .serializers import TaskSerializer, TaskPermissionSerializer
from .permissions import IsOwnerOrHasTaskPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrHasTaskPermission]


    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Task.objects.none()

        return Task.objects.filter(
            Q(owner=user) |
            Q(permissions__user=user)  # <-- правильно!
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskPermissionViewSet(viewsets.ModelViewSet):
    queryset = TaskPermission.objects.all()
    serializer_class = TaskPermissionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        task_id = request.data.get("task")
        task = Task.objects.get(id=task_id)
        if task.owner != request.user:
            return Response({"detail": "Only owner can share permissions."}, status=403)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        perm = self.get_object()
        if perm.task.owner != request.user:
            return Response({"detail": "Only owner can revoke permissions."}, status=403)
        return super().destroy(request, *args, **kwargs)


class RegisterView(APIView):
    """
    Регистрирует нового пользователя по username и password
    """
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "username already taken"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create(
            username=username,
            password=make_password(password)  # обязательно хэшируем!
        )

        return Response(
            {"message": "user registered"},
            status=status.HTTP_201_CREATED
        )
