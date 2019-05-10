"""Functional Tests === Acceptance Test === End-to-End test
These are our 'black box tests'
each section should follow an human readable 'user story'
"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import os

MAX_WAIT = 10


class DashboardTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    # Edith opens the website to service/
    # she is greeted with a dashboard that has a login request
    # She logs in and sees options to log new events
    # review outstanding events
    # and a menu with additional options
