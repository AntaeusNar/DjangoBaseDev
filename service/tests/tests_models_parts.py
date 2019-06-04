from django.test import TestCase
from service.models import MasterPart, Part, Manufacturer

# These Tests are for Parts and Part related items


class MasterPartModelTest(TestCase):

    def create_master_part(self, name='test name'):
        return MasterPart.objects.create(name=name)

    def test_creating_and_retrieving_master_part(self):
        mp = self.create_master_part()
        self.assertTrue(isinstance(mp, MasterPart))
        mp.save()

        saved_mps = MasterPart.objects.all()
        self.assertEqual(saved_mps.count(), 1)

        first_saved_mp = saved_mps[0]
        self.assertEqual(first_saved_mp.name, 'test name')


class PartModelTest(TestCase):

    def create_part(self, name='test name'):
        return Part.objects.create(name=name)

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


class ManufacturerModelTest(TestCase):

    def test_creating_and_retrieving_Manufacturers(self):
        manufacturer = Manufacturer()
        manufacturer.name = "John's Woodshop"
        manufacturer.save()

        saved_manufacturers = Manufacturer.objects.all()
        self.assertEqual(saved_manufacturers.count(), 1)

        first_saved_manufacturer = saved_manufacturers[0]
        self.assertEqual(first_saved_manufacturer.name, "John's Woodshop")
