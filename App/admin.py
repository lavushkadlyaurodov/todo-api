from django.contrib import admin
from .models import Task, TaskPermission  # Импортируй модели

admin.site.register(Task)
admin.site.register(TaskPermission)
