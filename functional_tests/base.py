import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        "Установка"
        self.toDoList = [
            "Купить павлиньи перья",
            "Сделать мушку из павлиньих перев",
            "Купить молоко"
        ]
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get("STAGING_SERVER")
        staging_port = os.environ.get("STAGING_PORT")
        if staging_server:
            self.live_server_url = f"http://{staging_server}"
        if staging_port:
            self.live_server_url += f":{staging_port}"
        self.MAX_WAIT = 10
        self.MIN_WAIT = 0.1

    def tearDown(self):
        "Демонтаж"
        self.browser.quit()

    def imputToDo(self, toDo):
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")
        inputbox.send_keys(toDo)
        inputbox.send_keys(Keys.ENTER)

    def checkRowInToDoTabel(self, rowText):
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

