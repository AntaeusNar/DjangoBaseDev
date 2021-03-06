from django.test import TestCase
from service.models import MasterPart, Part, Manufacturer, Supplier, SupplierPart, Address
from service.tests.tests_models_addresses import AddressModelTest
# These Tests are for Parts and Part related items


class SupplierModelTest(TestCase):

    def create_supplier(self, name='test supplier'):
        return Supplier.objects.create(name=name)

    def test_creating_and_retrieving_Suppliers(self):
        supplier = self.create_supplier(name="Bob's Supplies")
        self.assertTrue(isinstance(supplier, Supplier))
        supplier.save()

        saved_suppliers = Supplier.objects.all()
        self.assertEqual(saved_suppliers.count(), 1)

        first_saved_supplier = saved_suppliers[0]
        self.assertEqual(first_saved_supplier.name, "Bob's Supplies")
        self.assertEqual(first_saved_supplier.name, str(first_saved_supplier))

    def test_adding_an_address_to_supplier(self):
        kwargs = {
            "house_number": "3509",
            "road": "pelican brief ln",
            "postcode": "89084",
            "city": "north las vegas",
            "state": "nevada"}
        amt = AddressModelTest
        alpha_address = AddressModelTest.create_address(amt, **kwargs)
        self.assertTrue(isinstance(alpha_address, Address))
        alpha_address.save()

        supplier = self.create_supplier(name="Jed's Lab")
        self.assertTrue(isinstance(supplier, Supplier))
        supplier.save()

        supplier.address.add(alpha_address)

        saved_suppliers = Supplier.objects.all()
        self.assertEqual(saved_suppliers.count(), 1)

        first_saved_supplier = saved_suppliers[0]
        self.assertEqual(first_saved_supplier.address.all()[0].city, "North Las Vegas")


class ManufacturerModelTest(TestCase):

    def create_manufacturer(self, name='test name'):
        return Manufacturer.objects.create(name=name)

    def test_creating_and_retrieving_Manufacturers(self):
        manufacturer = self.create_manufacturer(name="John's Woodshop")
        self.assertTrue(isinstance(manufacturer, Manufacturer))
        manufacturer.save()

        saved_manufacturers = Manufacturer.objects.all()
        self.assertEqual(saved_manufacturers.count(), 1)

        first_saved_manufacturer = saved_manufacturers[0]
        self.assertEqual(first_saved_manufacturer.name, "John's Woodshop")
        self.assertEqual(first_saved_manufacturer.name, str(first_saved_manufacturer))

    def test_adding_address_to_manufacturer(self):
        kwargs = {
            "house_number": "3509",
            "road": "pelican brief ln",
            "postcode": "89084",
            "city": "north las vegas",
            "state": "nevada"}
        amt = AddressModelTest
        alpha_address = AddressModelTest.create_address(amt, **kwargs)
        self.assertTrue(isinstance(alpha_address, Address))
        alpha_address.save()

        manufacturer = self.create_manufacturer(name="Jed's Lab")
        self.assertTrue(isinstance(manufacturer, Manufacturer))
        manufacturer.save()

        manufacturer.address.add(alpha_address)

        saved_manufacturers = Manufacturer.objects.all()
        self.assertEqual(saved_manufacturers.count(), 1)

        first_saved_manufacturer = saved_manufacturers[0]
        self.assertEqual(first_saved_manufacturer.address.all()[0].city, "North Las Vegas")


class MasterPartModelTest(TestCase):

    def create_master_part(self, name='test name', man_name='test manufacturer',
                           man_part_num="test manufacturer part number"):
        man = Manufacturer.objects.create(name=man_name)
        return MasterPart.objects.create(name=name, manufacturer=man, man_part_num=man_part_num)

    def test_creating_and_retrieving_master_part(self):
        mp = self.create_master_part()
        self.assertTrue(isinstance(mp, MasterPart))
        mp.save()

        saved_mps = MasterPart.objects.all()
        self.assertEqual(saved_mps.count(), 1)

        first_saved_mp = saved_mps[0]
        self.assertEqual(first_saved_mp.name, 'test name')
        self.assertEqual(first_saved_mp.manufacturer.name, 'test manufacturer')
        self.assertEqual(first_saved_mp.man_part_num, 'test manufacturer part number')
        self.assertEqual(first_saved_mp.name, str(first_saved_mp))

    def test_add_supplier_to_master_parts(self):
        first_part = self.create_master_part()
        SMT = SupplierModelTest
        first_supplier = SupplierModelTest.create_supplier(SMT, name="Bob's Supplies")
        first_part.save()
        first_supplier.save()
        master_part_supplier = SupplierPart.objects.create(master_part=first_part, supplier=first_supplier, supplier_part_number="12345")

        saved_master_parts = MasterPart.objects.all()
        self.assertEqual(saved_master_parts.count(), 1)

        first_save_master_part = saved_master_parts[0]
        self.assertEqual(first_save_master_part.supplier.all()[0], first_supplier)
        self.assertEqual(first_save_master_part.supplier_part_number.all()[0].supplier_part_number, "12345")


class PartModelTest(TestCase):

    def create_part(self, name='test name', mp_name='master test name', man_name='test manufacturer'):
        man = Manufacturer.objects.create(name=man_name)
        mp = MasterPart.objects.create(name=mp_name, manufacturer=man)
        return Part.objects.create(name=name, master_part=mp)

    def test_creating_and_retrieving_parts(self):
        first_part = self.create_part(name='Flux Capacitor')
        self.assertTrue(isinstance(first_part, Part))
        first_part.save()

        saved_parts = Part.objects.all()
        self.assertEqual(saved_parts.count(), 1)

        first_saved_part = saved_parts[0]
        self.assertEqual(first_saved_part.name, 'Flux Capacitor')
        self.assertEqual(first_saved_part.name, str(first_saved_part))

    def test_add_parts_to_parts(self):
        first_part = self.create_part(name='Command Access Motor')
        second_part = self.create_part(name='RB12/24')
        parent_part = self.create_part(name="Von Duprin Panic Bar")
        first_part.save()
        second_part.save()
        parent_part.save()

        parent_part.subpart.add(first_part)
        parent_part.subpart.add(second_part)

        saved_parts = Part.objects.all()
        self.assertEqual(saved_parts.count(), 3)
        saved_parent_part = saved_parts[2]
        self.assertEqual(saved_parent_part.subpart.all()[0], first_part)
        self.assertEqual(saved_parent_part.subpart.all()[1], second_part)

