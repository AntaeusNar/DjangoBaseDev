from django.test import TestCase
from django.urls import resolve
from baseindex.views import index

# Create your tests here.


class IndexViewTest(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_view_uses_index_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'baseindex/index.html')
