from django.test import TestCase
from service.models import Event, Part, Container, Address
from service.tests.tests_models_parts import PartModelTest
import datetime

# Create your tests here.

# Todo: expand a Catagory or tag model to set things as client, accress control, you know grupings
class EventModelTest(TestCase):
    # Current rendition of an event:
    # A description of [an action] performed on [Group of Parts at a location/place] at a [time]

    def test_saving_and_retrieving_events(self):

        apartments_parts_group = Container()
        apartments_parts_group.name = "These parts at the Apartments"
        apartments_parts_group.save()

        this_today = datetime.date.today().strftime('%Y-%m-%d')
        yesterday = datetime.date.today() + datetime.timedelta(-1)
        # yesterday = yesterday.strftime('%Y-%m-%d')

        first_event = Event()
        first_event.description = "Felix fixed 3 windows and one door over at the apartments yesterday"
        first_event.action = "Repaired"
        first_event.status = "Active"
        first_event.container = apartments_parts_group
        first_event.event_date = yesterday
        first_event.save()

        saved_events = Event.objects.all()
        self.assertEqual(saved_events.count(), 1)

        first_saved_event = saved_events[0]
        self.assertEqual(
            first_saved_event.description,
            "Felix fixed 3 windows and one door over at the apartments yesterday"
        )
        self.assertEqual(first_saved_event.action, "Repaired")
        self.assertEqual(first_saved_event.status, 'Active')
        self.assertEqual(first_saved_event.container, apartments_parts_group)
        self.assertEqual(first_saved_event.event_date, yesterday)
        # Todo: Somehow sometimes this is off by one day
        self.assertEqual(first_saved_event.rec_date.strftime('%Y-%m-%d'), this_today)


class ContainerModelTest(TestCase):

    def test_creating_and_retrieving_containers_with_Subcontainers(self):
        first_container = Container()
        first_container.name = 'Tardis'
        first_container.save()

        second_container = Container()
        second_container.name = "England"
        second_container.save()
        second_container.subcontainer.add(first_container)

        saved_containers = Container.objects.all()
        self.assertEqual(saved_containers.count(), 2)

        first_saved_container = saved_containers[0]
        self.assertEqual(first_saved_container.name, 'Tardis')

        second_saved_container = saved_containers[1]
        self.assertEqual(second_saved_container.name, 'England')
        self.assertEqual(second_saved_container.subcontainer.all()[0], first_container)
        self.assertEqual(second_saved_container.subcontainer.all()[0], first_saved_container)
        self.assertEqual(second_saved_container.name, str(second_saved_container))

        third_container = Container()
        third_container.name = "UK"
        third_container.save()
        third_container.subcontainer.add(first_container)
        third_container.subcontainer.add(second_container)

        self.assertEqual(third_container.subcontainer.all()[0], first_container)
        self.assertEqual(third_container.subcontainer.all()[1], second_container)

    def test_creating_containers_with_addresses(self):

        first_address = Address()
        first_address.house_number = '3509'
        first_address.road = 'Pelican Brief Ln'
        first_address.postcode = '89084'
        first_address.city = 'North Las Vegas'
        first_address.state = 'Nevada'
        first_address.country = 'USA'
        first_address.save()

        first_container = Container()
        first_container.name = 'Tardis'
        first_container.save()
        first_container.address.add(first_address)

        saved_containers = Container.objects.all()
        self.assertEqual(saved_containers.count(), 1)

        first_saved_container = saved_containers[0]
        self.assertEqual(first_saved_container.address.all()[0].city, 'North Las Vegas')

    def test_adding_parts_to_containers(self):

        PMT = PartModelTest
        first_part = PartModelTest.create_part(PMT, name="Trebuchet")
        second_part = PartModelTest.create_part(PMT, name="Horcrux")
        first_part.save()
        second_part.save()

        saved_parts = Part.objects.all()
        self.assertEqual(saved_parts.count(), 2)

        first_container = Container()
        first_container.name = "Bag of Holding"
        first_container.save()

        saved_containers = Container.objects.all()
        self.assertEqual(saved_containers.count(), 1)

        first_saved_container = saved_containers[0]
        first_saved_container.part.add(first_part)
        first_saved_container.part.add(second_part)
        self.assertEqual(first_saved_container.part.count(), 2)
        self.assertEqual(first_saved_container.part.all()[0], first_part)
        self.assertEqual(first_saved_container.part.all()[1], second_part)
