from django.test import TestCase
from django.urls import resolve
from service.views import dashboard, register

# Create your tests here.


class IndexViewTest(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, dashboard)

    def test_index_view_uses_index_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'service/dashboard.html')


class LoginViewTest(TestCase):

    def test_login_uses_login_template(self):
        response = self.client.get('/accounts/login')
        self.assertTemplateUsed(response, 'registration/login.html')


class RegisterViewTest(TestCase):

    def test_register_url_resolves_to_register_view(self):
        found = resolve("/register")
        self.assertEqual(found.func, register)

    def test_register_uses_register_template(self):
        response = self.client.get('/accounts/register')
        self.assertTemplateUsed(response, 'registration/register.html')
