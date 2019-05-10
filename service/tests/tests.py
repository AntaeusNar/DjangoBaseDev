from django.test import TestCase
from django.urls import resolve
from service.views import dashboard
from service.models import Event, Part

# Create your tests here.


class IndexViewTest(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/service/')
        self.assertEqual(found.func, dashboard)

    def test_index_view_uses_index_template(self):
        response = self.client.get('/service/')
        self.assertTemplateUsed(response, 'service/dashboard.html')


class EventModelTest(TestCase):

    def test_saving_and_retrieving_events(self):

        first_event = Event()
        first_event.title = "The first event"
        first_event.description = "This is a test of the first event description"
        first_event.category = "Install"

        first_event.save()

        saved_events = Event.objects.all()
        self.assertEqual(saved_events.count(), 1)

        first_saved_event = saved_events[0]
        self.assertEqual(first_saved_event.title, 'The first event')
        self.assertEqual(first_saved_event.description, "This is a test of the first event description")
        self.assertEqual(first_saved_event.category, 'Install')


class PartModelTest(TestCase):

    def test_creating_and_retrieving_parts(self):

        first_part = Part()
        first_part.name = "Flux Capacitor"

        first_part.save()

        saved_parts = Part.objects.all()
        self.assertEqual(saved_parts.count(), 1)

        first_saved_part = saved_parts[0]
        self.assertEqual(first_saved_part.name, 'Flux Capacitor')