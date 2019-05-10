from django.test import TestCase
from service.models import Event, Part, Container
import datetime

# Create your tests here.


class EventModelTest(TestCase):
    # Current rendition of an event:
    # A description of [an action] performed on [Group of Parts] at a [location/place] at a [time]

    def test_saving_and_retrieving_events(self):

        parts_group = "these things"
        apartments = 'The Apartments'
        yesterday = 'Oct the 10th at 11 in the morning'
        today = 'Dec. 7th 546'

        first_event = Event()
        first_event.description = "Felix fixed 3 windows and one door over at the apartments yesterday"
        first_event.action = "Installed"
        first_event.parts_group = parts_group
        first_event.container = apartments
        first_event.event_date = yesterday
        first_event.rec_date = today
        first_event.save()

        saved_events = Event.objects.all()
        self.assertEqual(saved_events.count(), 1)

        first_saved_event = saved_events[0]
        self.assertEqual(
            first_saved_event.description,
            "Felix fixed 3 windows and one door over at the apartments yesterday"
        )
        self.assertEqual(first_saved_event.action, "Installed")
        self.assertEqual(first_saved_event.parts_group, parts_group)
        self.assertEqual(first_saved_event.container, apartments)
        self.assertEqual(first_saved_event.event_date, yesterday)
        self.assertEqual(first_saved_event.rec_date, today)


class PartModelTest(TestCase):

    def test_creating_and_retrieving_parts(self):
        first_part = Part()
        first_part.name = "Flux Capacitor"

        first_part.save()

        saved_parts = Part.objects.all()
        self.assertEqual(saved_parts.count(), 1)

        first_saved_part = saved_parts[0]
        self.assertEqual(first_saved_part.name, 'Flux Capacitor')


class ContainerModelTest(TestCase):

    def test_creating_and_retrieving_containers(self):
        first_container = Container()
        first_container.name = 'Tardis'
        first_container.save()

        second_container = Container()
        second_container.name = "England"
        second_container.subcontainer = first_container
        second_container.save()

        saved_containers = Container.objects.all()
        self.assertEqual(saved_containers.count(), 2)

        first_saved_container = saved_containers[0]
        self.assertEqual(first_saved_container.name, 'Tardis')

        second_saved_container = saved_containers[1]
        self.assertEqual(second_saved_container.name, 'England')
        self.assertEqual(second_saved_container.subcontainer, first_container)
        self.assertEqual(second_saved_container.subcontainer, first_saved_container)

    def test_adding_parts_to_new_container(self):
        first_part = Part()
        first_part.name = "Trebuchet"
        first_part.save()

        second_part = Part()
        second_part.name = "Horcrux"
        second_part.save()

        saved_parts = Part.objects.all()
        self.assertEqual(saved_parts.count(), 2)

        first_container = Container()
        first_container.name = 'Tardis'
        first_container.save()

        second_container = Container()
        second_container.name = "England"
        second_container.subcontainer = first_container
        second_container.save()

        saved_containers = Container.objects.all()
        self.assertEqual(saved_containers.count(), 2)