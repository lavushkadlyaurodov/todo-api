from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

class TaskPermission(models.Model):
    PERMISSION_CHOICES = (
        ('read', 'Read'),
        ('update', 'Update'),
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_permissions')
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = ('task', 'user', 'permission')
