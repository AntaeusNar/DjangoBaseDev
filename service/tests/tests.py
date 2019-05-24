from django.test import TestCase
from django.urls import resolve, reverse
from service.views import dashboard, registration
from django.contrib.auth.models import User

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
        response = self.client.get('/accounts/login/')
        self.assertTemplateUsed(response, 'registration/login.html')


class RegistrationViewTest(TestCase):

    def test_registration_url_resolves_to_register_view(self):
        found = resolve('/accounts/registration/')
        self.assertEqual(found.func, registration)

    def test_registration_uses_register_template(self):
        response = self.client.get('/accounts/registration/')
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_can_save_a_POST_request(self):
        self.client.post(reverse('registration'), data={'username': 'FishyTom',
                                                        'password1': 'horsesaremadeofpoop',
                                                        'password2': 'horsesaremadeofpoop'})
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.username, 'FishyTom')

    def test_registration_POST_can_build_a_full_user(self):
        user1 = {'username': 'UglyPaul@test.com',
                 'password1': 'yourmomisaboat',
                 'password2': 'yourmomisaboat',
                 'email': 'Ugly.Paul@test.com',
                 'first_name': 'Paul',
                 'last_name': 'Ugly'}
        self.client.post(reverse('registration'), data=user1)
        self.assertEqual(User.objects.count(), 1)
        saved_user = User.objects.first()
        self.assertEqual(saved_user.username, 'UglyPaul@test.com')
        self.assertEqual(saved_user.email, 'Ugly.Paul@test.com')
        self.assertEqual(saved_user.first_name, 'Paul')
        self.assertEqual(saved_user.last_name, 'Ugly')
