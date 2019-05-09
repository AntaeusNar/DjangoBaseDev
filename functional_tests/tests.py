"""Functional Tests === Acceptance Test === End-to-End test
These are our 'black box tests'
each section should follow an human readable 'user story'
"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
import os

MAX_WAIT = 10


class IndexTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def test_index_page_loads(self):
        # Edith goes to the home page
        response = self.client.get(self.live_server_url)
        self.assertEqual(response.status_code, 200)

    def test_finish_functional_tests(self):
        self.fail('Finish the Functional Test!')
