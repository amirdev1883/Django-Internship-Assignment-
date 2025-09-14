from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import UserRegistrationForm, UserLoginForm


class UserRegistrationFormTest(TestCase):

    def setUp(self):
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='TestPassword123'
        )

    def test_registration_form_valid_data(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'MySecurePassword',
            'password2': 'MySecurePassword',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_email_exists(self):
        form_data = {
            'username': 'anotheruser',
            'email': 'existing@example.com',
            'password1': 'MySecurePassword',
            'password2': 'MySecurePassword',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_registration_form_passwords_do_not_match(self):
        form_data = {
            'username': 'newuser',
            'email': 'unique@example.com',
            'password1': 'password123',
            'password2': 'password456',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)  

    def test_registration_form_missing_fields(self):
        form_data = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)


class UserLoginFormTest(TestCase):

    def test_login_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'password': 'securepass',
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_missing_username(self):
        form_data = {
            'username': '',
            'password': 'securepass',
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_login_form_missing_password(self):
        form_data = {
            'username': 'testuser',
            'password': '',
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
