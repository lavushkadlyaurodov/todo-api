from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import TaskPermission

class IsOwnerOrHasTaskPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        if request.method in SAFE_METHODS:
            return TaskPermission.objects.filter(task=obj, user=request.user, permission='read').exists()
        if request.method in ['PUT', 'PATCH']:
            return TaskPermission.objects.filter(task=obj, user=request.user, permission='update').exists()
        return False