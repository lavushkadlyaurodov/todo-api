from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TaskPermissionViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'task-permissions', TaskPermissionViewSet, basename='taskpermission')

urlpatterns = [
    path('', include(router.urls)),  # здесь маршруты к Task и TaskPermission
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
