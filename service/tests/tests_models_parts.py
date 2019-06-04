from django.test import TestCase
from service.models import Part

# These Tests are for Parts and Part related items


class PartModelTest(TestCase):

    def test_creating_and_retrieving_parts(self):
        first_part = Part()
        first_part.name = "Flux Capacitor"

        first_part.save()

        saved_parts = Part.objects.all()
        self.assertEqual(saved_parts.count(), 1)

        first_saved_part = saved_parts[0]
        self.assertEqual(first_saved_part.name, 'Flux Capacitor')
        self.assertEqual(first_saved_part.name, str(first_saved_part))

    def test_add_parts_to_parts(self):
        first_part = Part()
        first_part.name = "Command Access Motor"

        first_part.save()

        second_part = Part()
        second_part.name = "RB12/24"

        second_part.save()

        parent_part = Part()
        parent_part.name = "Von Duprin Panic Bar"
        parent_part.save()
        parent_part.subpart.add(first_part)
        parent_part.subpart.add(second_part)

        saved_parts = Part.objects.all()
        self.assertEqual(saved_parts.count(), 3)
        saved_parent_part = saved_parts[2]
        self.assertEqual(saved_parent_part.subpart.all()[0], first_part)
        self.assertEqual(saved_parent_part.subpart.all()[1], second_part)