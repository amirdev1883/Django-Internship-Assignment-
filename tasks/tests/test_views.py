from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
from datetime import date


class TaskViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.other_user = User.objects.create_user(username='user2', password='pass')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test description',
            due_date=date.today(),
            owner=self.user
        )

    def test_create_task_post_valid(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('tasks:task_create'), {
            'title': 'New Task',
            'description': 'New description',
            'due_date': date.today(),
            'completed': False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)

    def test_update_own_task(self):
        self.client.login(username='user1', password='pass')
        url = reverse('tasks:task_update', args=[self.task.id])
        response = self.client.post(url, {
            'title': 'Updated',
            'description': 'Updated desc',
            'due_date': date.today(),
            'completed': True,
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated')

    def test_update_other_users_task_redirect(self):
        self.client.login(username='user2', password='pass')
        url = reverse('tasks:task_update', args=[self.task.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('tasks:home'))

    def test_view_own_task(self):
        self.client.login(username='user1', password='pass')
        url = reverse('tasks:task_detail', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_other_users_task_forbidden(self):
        self.client.login(username='user2', password='pass')
        url = reverse('tasks:task_detail', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  

    def test_list_user_tasks(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
