from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Task

class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.client.login(username='test', password='pass')

    def test_create_task(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/tasks/', {
            'title': 'Test Task',
            'description': 'Some description'
        })
        self.assertEqual(response.status_code, 201)
