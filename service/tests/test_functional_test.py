"""Functional Tests === Acceptance Test === End-to-End test
These are our 'black box tests'
each section should follow an human readable 'user story'
"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import os
import time

MAX_WAIT = 10


class DashboardTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        else:
            self.live_server_url = self.live_server_url

    def tearDown(self):
        self.browser.quit()

    def helper_wait_for_row_in_table(self, row_text, table_id='id_list_table'):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id(table_id)
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (WebDriverException, NoSuchElementException) as e:
                if time.time() - start_time > MAX_WAIT:
                    self.fail(e)
                time.sleep(0.5)
            except AssertionError as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                    time.sleep(0.5)

    def test_service_page_loads(self):
        # Edith opens the website to service/
        response = self.client.get(self.live_server_url)
        self.assertEqual(response.status_code, 200)

    def test_login_option_loads(self):
        # she is greeted with a login option
        self.browser.get(self.live_server_url)
        nav_bar = self.browser.find_element_by_id('collapsibleNavbar').get_attribute("innerHTML").strip()
        self.assertInHTML('Login', nav_bar)

    def test_latest_events_displayed(self):
        # Edith logs in and sees a section for recent events
        self.browser.get(self.live_server_url)
        header4_text = self.browser.find_element_by_tag_name('h4').text
        self.assertIn('Most Recently Closed', header4_text)
        # She sees that by default the last 10 events are listed here
        self.helper_wait_for_row_in_table('1:', 'id_events_table')
        self.helper_wait_for_row_in_table('10', 'id_events_table')

        self.fail('Finish Events Display')
        # There is an option to change how many events are shown
        # and filtering options based on names, dates, parts and addresses

    def test_finish_fail(self):
        self.fail('Finish Functional Test of Service')

