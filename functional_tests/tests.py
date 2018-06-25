import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        "Установка"
        self.toDoList = [
            "Купить павлиньи перья",
            "Сделать мушку из павлиньих перев",
            "Купить молоко"
        ]
        self.browser = webdriver.Firefox()
        self.MAX_WAIT = 2
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

    def test_can_start_a_list_for_one_user(self):

        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn('To-Do', header_text)

        self.imputToDo(self.toDoList[0])
        self.checkRowInToDoTabel(f"1: {self.toDoList[0]}")

        self.imputToDo(self.toDoList[1])
        self.checkRowInToDoTabel(f"2: {self.toDoList[1]}")

    def test_multiple_users_can_start_lists_at_different_urls(self):

        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn('To-Do', header_text)

        self.imputToDo(self.toDoList[0])
        self.checkRowInToDoTabel(f"1: {self.toDoList[0]}")

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn( self.toDoList[0], page_text)
        self.assertNotIn( self.toDoList[1], page_text)

        self.imputToDo(self.toDoList[2])
        self.checkRowInToDoTabel(f"1: {self.toDoList[2]}")

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn(self.toDoList[0], page_text)
        self.assertIn(self.toDoList[2], page_text)
