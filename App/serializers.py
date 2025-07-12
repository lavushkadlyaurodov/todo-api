from rest_framework import serializers
from .models import Task, TaskPermission

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']

class TaskPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPermission
        fields = '__all__'