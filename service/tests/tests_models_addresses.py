from django.test import TestCase
from service.models import Address


class AddressModelTest(TestCase):

    def create_address(self, postcode="89084", city="North Las Vegas", state="NV", **kwargs):
        return Address.objects.create(postcode=postcode, city=city, state=state, **kwargs)

    def test_creating_and_retrieving_addresses(self):
        kwargs = {
            "house_number": "3509",
            "road": "Pelican Brief Ln",
            "postcode": "89084",
            "city": "North Las Vegas",
            "state": "NV"}
        alpha_address = self.create_address(**kwargs)
        self.assertTrue(isinstance(alpha_address, Address))
        alpha_address.save()

        saved_addresses = Address.objects.all()
        self.assertEqual(saved_addresses.count(), 1)

        first_saved_address = saved_addresses[0]
        self.assertEqual(first_saved_address.house_number, '3509')
        self.assertEqual(first_saved_address.road, 'Pelican Brief Ln')
        self.assertEqual(first_saved_address.postcode, '89084')
        self.assertEqual(first_saved_address.city, 'North Las Vegas')
        self.assertEqual(first_saved_address.state, 'NV')

        self.assertEqual(str(first_saved_address), '3509 Pelican Brief Ln, North Las Vegas, NV 89084')

    def test_modified_save_function_change_formatting(self):
        kwargs = {
            "house_number": "3509",
            "road": "pelican brief ln",
            "postcode": "89084",
            "city": "north las vegas",
            "state": "nevada"}
        alpha_address = self.create_address(**kwargs)
        self.assertTrue(isinstance(alpha_address, Address))
        alpha_address.save()

        saved_addresses = Address.objects.all()
        self.assertEqual(saved_addresses.count(), 1)

        first_saved_address = saved_addresses[0]
        self.assertEqual(first_saved_address.house_number, '3509')
        self.assertEqual(first_saved_address.road, 'Pelican Brief Ln')
        self.assertEqual(first_saved_address.postcode, '89084')
        self.assertEqual(first_saved_address.city, 'North Las Vegas')
        self.assertEqual(first_saved_address.state, 'NV')

        self.assertEqual(str(first_saved_address), '3509 Pelican Brief Ln, North Las Vegas, NV 89084')

    def test_modified_save_function_pobox_vs_house(self):

        first_address = Address()
        first_address.house_number = '3509'
        first_address.road = 'pelican brief ln'
        first_address.postcode = '89084'
        first_address.city = "north las vegas"
        first_address.state = 'nevada'

        first_address.save()

        second_address = Address()
        second_address.po_box = '17'
        second_address.city = 'henderson'
        second_address.state = 'nv'
        second_address.postcode = '89119'

        second_address.save()

        saved_addresses = Address.objects.all()
        self.assertEqual(saved_addresses.count(), 2)

        first_saved_address = saved_addresses[0]
        second_saved_address = saved_addresses[1]

        self.assertEqual(str(first_saved_address), '3509 Pelican Brief Ln, North Las Vegas, NV 89084')
        self.assertEqual(str(second_saved_address), 'PO Box 17, Henderson, NV 89119')

    def test_save_unit_address(self):

        first_address = Address()
        first_address.house_number = '3509'
        first_address.road = 'pelican brief ln'
        first_address.unit = '2B'
        first_address.postcode = '89084'
        first_address.city = "north las vegas"
        first_address.state = 'nevada'

        first_address.save()

        saved_addresses = Address.objects.all()
        first_saved_address = saved_addresses[0]
        self.assertEqual(str(first_saved_address), '3509 Pelican Brief Ln, 2B, North Las Vegas, NV 89084')

    def test_modified_save_function_super_save(self):

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
        first_saved_address.house_number = '3520'
        first_saved_address.save(update_fields=['house_number'])

        self.assertEqual(str(first_saved_address), '3520 Pelican Brief Ln, North Las Vegas, NV 89084')

        second_address = Address()
        second_address.po_box = '17'
        second_address.city = 'henderson'
        second_address.state = 'nv'
        second_address.postcode = '89119'
        second_address.county = 'Clark'
        second_address.save()

        saved_addresses = Address.objects.all()
        self.assertEqual(saved_addresses.count(), 2)

        second_saved_address = saved_addresses[1]
        self.assertEqual(second_saved_address.county, 'Clark')