from django.test import TestCase
from django.urls import resolve, reverse
from service.views import dashboard, registration, create_event
from django.contrib.auth.models import User
from service.models import Event

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
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')


class CreateEventsViewTest(TestCase):

    def test_create_event_url_resolves_to_create_event_view(self):
        found = resolve(reverse('create_event'))
        self.assertEqual(found.func, create_event)

    def test_create_event_uses_create_event_template(self):
        response = self.client.get(reverse('create_event'))
        self.assertTemplateUsed(response, 'service/create_event.html')

    def test_create_event_POST_can_create_event(self):
        address = {'house_number': '3509',
                   'road': 'Pelican Brief Ln',
                   'postcode': '89084',
                   'city': 'North Las Vegas',
                   'state': 'NV',
                   'country': 'USA',
                   }
        part = {'name': 'Fishing Pole'}
        container = {'name': 'First Location',
                     'part': part,
                     'address': address,
                     }
        event = {'action': 'Add',
                 'status': 'Active',
                 'container': container,
                 }
        self.client.post(reverse('create_event'), data=event)
        self.assertEqual(Event.objects.count(), 1)


class RegistrationViewTest(TestCase):

    def test_registration_url_resolves_to_register_view(self):
        found = resolve(reverse('registration'))
        self.assertEqual(found.func, registration)

    def test_registration_uses_register_template(self):
        response = self.client.get(reverse('registration'))
        self.assertTemplateUsed(response, 'registration/register.html')

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
