import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from lists.forms import PLACE_HOLDER


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
        staging_server = os.environ.get("STAGING_SERVER")
        staging_port = os.environ.get("STAGING_PORT")
        if staging_server:
            self.live_server_url = f"http://{staging_server}"
        if staging_port:
            self.live_server_url += f":{staging_port}"
        self.MAX_WAIT = 2
        self.MIN_WAIT = 0.1

    def tearDown(self):
        "Демонтаж"
        self.browser.quit()

    def get_item_input_box(self):
        startTime = time.time()
        while True:
            try:
                return self.browser.find_element_by_id("id_text")
            except (AssertionError, WebDriverException) as ex:
                if time.time() - startTime > self.MAX_WAIT:
                    raise ex
                time.sleep(self.MIN_WAIT)

    def imputToDo(self, toDo):
        inputbox = self.get_item_input_box()
        placeholder_text = inputbox.get_attribute("placeholder")
        self.assertEqual(placeholder_text, PLACE_HOLDER)
        inputbox.send_keys(toDo)
        inputbox.send_keys(Keys.ENTER)

    def wait_for_row_in_list_table(self, rowText):
        startTime = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(rowText, [row.text for row in rows])
            except (AssertionError, WebDriverException) as ex:
                if time.time() - startTime > self.MAX_WAIT:
                    raise ex
                time.sleep(self.MIN_WAIT)
            else:
                return

    def wait_for(self, fn):
        startTime = time.time()
        # step = 1
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as ex:
                if time.time() - startTime > self.MAX_WAIT:
                    raise ex
                time.sleep(self.MIN_WAIT)
                # print(f"waiting step: {step}")
                # step += 1
            else:
                return

    def wait_to_be_logged_in(self, email):
        self.wait_for(lambda : self.browser.find_element_by_link_text("Log out"))
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for(lambda : self.browser.find_element_by_name("email"))
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)
