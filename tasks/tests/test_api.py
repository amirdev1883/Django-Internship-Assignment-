from rest_framework.test import APITestCase
from django.urls import reverse
from tasks.models import Task
from django.contrib.auth.models import User
from datetime import date

class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass")
        self.other_user = User.objects.create_user(username="user2", password="pass")

        self.task = Task.objects.create(
            title="My Task",
            description="Desc",
            due_date=date.today(),
            completed=False,
            owner=self.user
        )

        self.client.login(username="user1", password="pass")

    def test_get_tasks_list(self):
        response = self.client.get(reverse("tasks:api_task_list_create"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "My Task")

    def test_create_task(self):
        data = {
            "title": "API Task",
            "description": "Test",
            "due_date": str(date.today()),
            "completed": False,
        }
        response = self.client.post(reverse("tasks:api_task_list_create"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.filter(owner=self.user).count(), 2)

    def test_update_own_task(self):
        url = reverse("tasks:api_task_detail", args=[self.task.id])
        data = {
            "title": "Updated",
            "description": "Updated Desc",
            "due_date": str(date.today()),
            "completed": True,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated")

    def test_update_other_users_task_forbidden(self):
        self.client.logout()
        self.client.login(username="user2", password="pass")
        url = reverse("tasks:api_task_detail", args=[self.task.id])
        response = self.client.put(url, {
            "title": "Hack",
            "description": "Hack",
            "due_date": str(date.today()),
            "completed": False
        })
        self.assertEqual(response.status_code, 404)

    def test_delete_own_task(self):
        url = reverse("tasks:api_task_detail", args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_other_users_task(self):
        self.client.logout()
        self.client.login(username="user2", password="pass")
        url = reverse("tasks:api_task_detail", args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
