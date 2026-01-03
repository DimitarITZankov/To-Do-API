# Tests for the Tasks API

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from core import models
from tasks import serializers

TASKS_URL = reverse('tasks-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_task(user, **params):
    defaults = {
        'title': 'Sample task',
        'public': True,
        'completed': False,
    }
    defaults.update(params)
    return models.Tasks.objects.create(user=user, **defaults)


class PublicTasksApiTests(TestCase):
    """Tests for /api/tasks/tasks/ endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@test.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_auth_required(self):
        """Unauthenticated users cannot access tasks"""
        self.client.force_authenticate(None)

        res = self.client.get(TASKS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_only_public_and_not_completed_tasks(self):
        """Only public & incomplete tasks are returned"""

        # Visible task
        task1 = create_task(
            user=self.user,
            title='Public task',
            public=True,
            completed=False
        )

        # Should NOT be visible
        create_task(
            user=self.user,
            title='Private task',
            public=False,
            completed=False
        )

        create_task(
            user=self.user,
            title='Completed task',
            public=True,
            completed=True
        )

        res = self.client.get(TASKS_URL)

        tasks = models.Tasks.objects.filter(
            public=True,
            completed=False
        )
        serializer = serializers.TasksSerializer(tasks, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], task1.title)

    def test_tasks_are_ordered_by_id(self):
        """Tasks are returned in correct order"""

        create_task(user=self.user, title='Task 1')
        create_task(user=self.user, title='Task 2')

        res = self.client.get(TASKS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
