import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from functional_tests.server_tools import reset_database
from lists.forms import PLACE_HOLDER

MAX_WAIT = 2
MIN_WAIT = 0.1


def wait(function):
    def modify_function(*args, **kwargs):
        startTime = time.time()
        while True:
            try:
                return function(*args, **kwargs)
            except (AssertionError, WebDriverException) as ex:
                if time.time() - startTime > MAX_WAIT:
                    raise ex
                time.sleep(MIN_WAIT)

    return modify_function


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        "Установка"
        self.toDoList = [
            "Купить павлиньи перья",
            "Сделать мушку из павлиньих перев",
            "Купить молоко"
        ]
        self.browser = webdriver.Firefox()
        # self.browser = webdriver.Chrome()
        self.staging_server = os.environ.get("STAGING_SERVER")
        self.staging_port = os.environ.get("STAGING_PORT")
        if self.staging_server:
            self.live_server_url = f"http://{self.staging_server}"
            if self.staging_port and str(self.staging_port) != '80':
                self.live_server_url += f":{self.staging_port}"
            reset_database(self.staging_server)

    def tearDown(self):
        "Демонтаж"
        self.browser.quit()

    def get_item_input_box(self):
        startTime = time.time()
        while True:
            try:
                return self.browser.find_element_by_id("id_text")
            except (AssertionError, WebDriverException) as ex:
                if time.time() - startTime > MAX_WAIT:
                    raise ex
                time.sleep(MIN_WAIT)

    def imputToDo(self, toDo):
        inputbox = self.get_item_input_box()
        placeholder_text = inputbox.get_attribute("placeholder")
        self.assertEqual(placeholder_text, PLACE_HOLDER)
        inputbox.send_keys(toDo)
        inputbox.send_keys(Keys.ENTER)

    @wait
    def wait_for_row_in_list_table(self, rowText):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(rowText, [row.text for row in rows])

    @wait
    def wait_for(self, function):
        return function()

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text("Log out")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name("email")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)
