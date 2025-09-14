from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_register_get(self):
        response = self.client.get(reverse('accounts:user_register'))
        self.assertEqual(response.status_code, 200)

    def test_register_post_valid(self):
        response = self.client.post(reverse('accounts:user_register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        self.assertRedirects(response, reverse('tasks:home'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_redirect_if_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('accounts:user_register'))
        self.assertRedirects(response, reverse('tasks:home'))

    def test_login_post_valid(self):
        response = self.client.post(reverse('accounts:user_login'), {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertRedirects(response, reverse('tasks:home'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_post_invalid(self):
        response = self.client.post(reverse('accounts:user_login'), {
            'username': 'testuser',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username or password is wrong')

    def test_login_redirect_if_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('accounts:user_login'))
        self.assertRedirects(response, reverse('tasks:home'))

    def test_logout_redirect(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('accounts:user_logout'))
        self.assertRedirects(response, reverse('tasks:home'))
        self.assertNotIn('_auth_user_id', self.client.session)
