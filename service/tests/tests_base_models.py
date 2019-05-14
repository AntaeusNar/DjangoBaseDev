from django.test import TestCase
from service.models import Event, Part, Container, PartQuantity, Address
import datetime

# Create your tests here.


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
        self.assertEqual(first_saved_event.container, apartments_parts_group)
        self.assertEqual(first_saved_event.event_date, yesterday)
        self.assertEqual(first_saved_event.rec_date.strftime('%Y-%m-%d'), this_today)


class AddressModelTest(TestCase):

    def test_creating_and_retrieving_addresses(self):

        first_address = Address()
        first_address.house_number = '3509'
        first_address.road = 'Pelican Brief Ln'
        first_address.postcode = '89084'
        first_address.city = "North Las Vegas"
        first_address.state = 'NV'

        first_address.save()

        saved_addresses = Address.objects.all()
        self.assertEqual(saved_addresses.count(), 1)

        first_saved_address = saved_addresses[0]
        self.assertEqual(first_saved_address.house_number, '3509')
        self.assertEqual(first_saved_address.road, 'Pelican Brief Ln')
        self.assertEqual(first_saved_address.postcode, '89084')
        self.assertEqual(first_saved_address.city, 'North Las Vegas')
        self.assertEqual(first_saved_address.state, 'NV')

        self.assertEqual(str(first_saved_address), '3509 Pelican Brief Ln, North Las Vegas, NV 89084')

    def test_modified_save_function(self):

        first_address = Address()


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

    def test_containers_in_containers(self):

        first_container = Container()
        first_container.name = 'Tardis'
        first_container.save()

        second_container = Container()
        second_container.name = "England"
        second_container.subcontainer = first_container
        second_container.save()

        saved_containers = Container.objects.all()
        self.assertEqual(saved_containers.count(), 2)

        second_saved_container = saved_containers[1]
        self.assertEqual(second_saved_container.subcontainer, first_container)

    def test_adding_parts_to_containers(self):

        first_part = Part()
        first_part.name = "Trebuchet"
        first_part.save()

        second_part = Part()
        second_part.name = "Horcrux"
        second_part.save()

        saved_parts = Part.objects.all()
        self.assertEqual(saved_parts.count(), 2)

        first_container = Container()
        first_container.name = "Bag of Holding"
        first_container.save()

        saved_containers = Container.objects.all()
        self.assertEqual(saved_containers.count(), 1)

        group_of_parts = PartQuantity.objects.create(part=first_part, container=first_container, amount=7)
        group_of_parts_2 = PartQuantity.objects.create(part=second_part, container=first_container, amount=24)

        first_saved_container = saved_containers[0]
        fsc_part_quantities = first_saved_container.part_quantity.all()
        self.assertEqual(fsc_part_quantities.count(), 2)

        first_fsc_part_quantity = fsc_part_quantities[0]
        self.assertEqual(first_fsc_part_quantity.part.name, 'Trebuchet')
        self.assertEqual(first_fsc_part_quantity.amount, 7)

        second_fsc_part_quantity = fsc_part_quantities[1]
        self.assertEqual(second_fsc_part_quantity.part.name, 'Horcrux')
        self.assertEqual(second_fsc_part_quantity.amount, 24)
