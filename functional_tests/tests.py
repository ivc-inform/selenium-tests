import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):


    def setUp(self):
        "Установка"
        self.toDoList = [
            "Купить павлиньи перья",
            "Сделать мушку из павлиньих перев"
        ]
        self.browser = webdriver.Firefox()

    def tearDown(self):
        "Демонтаж"
        self.browser.quit()

    def imputToDo(self, toDo):
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")
        inputbox.send_keys(toDo)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

    def checkRowInToDoTabel(self, rowText):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(rowText, [row.text for row in rows])

    def test_попробуем_статртануть_и_доделаем_позже(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn('To-Do', header_text)

        self.imputToDo(self.toDoList[0])
        self.imputToDo(self.toDoList[1])

        self.checkRowInToDoTabel(f"1: {self.toDoList[0]}")
        self.checkRowInToDoTabel(f"2: {self.toDoList[1]}")

        self.fail("Закончить тест ...")