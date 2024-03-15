from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from contacts.models import Contact
from tasks.models import Task, Topic
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.models import ResetPasswordToken

class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_user_url = reverse('registry')
        self.login_url = reverse('login')
        self.reset_user_pw_url = reverse('password_reset_confirm', args=['uidb64', 'token'])

        self.user_data = {
            'first_name': 'Firstname',
            'last_name': 'Lastname',
            'password': 'securepassword',
            'email': 'firstnamelastname@example.com',
        }

    def test_user_registration_and_login(self):
        response = self.client.post(self.create_user_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_data = {
            'email': 'firstnamelastname@example.com',
            'password': 'securepassword',
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class TaskApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.force_authenticate(user=self.user)
        self.tasks_url = reverse('tasks-list')

    def test_get_tasks(self):
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        topic = Topic.objects.create(title='test')
        assigned_client = Contact.objects.create(first_name='test')
        data = {
            "category": "test_category",
            "title": "test_title",
            "description": "test_desc",
            "date": "2024-01-16",
            "subtasks": {},
            "prio": "test",
            "topic": topic.id,
            "author": self.user.id,
            "assigned_clients": [assigned_client.id],
        }
        response = self.client.post(self.tasks_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'test_title')
        print(response.content)

    def test_update_task(self):
        task = Task.objects.create(title='new_test_title')
        data = {'id': task.id, 'title': 'old_test_title'}
        response = self.client.patch(self.tasks_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().title, 'old_test_title')

    def test_delete_task(self):
        task = Task.objects.create(title='delete_test_title')
        data = {'id': task.id}
        response = self.client.delete(self.tasks_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
