import time

from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        "Установка"
        self.browser = webdriver.Firefox()

    def tearDown(self):
        "Демонтаж"
        self.browser.quit()

    def test_попробуем_статртануть_и_доделаем_позже(self):
        self.browser.get("http://localhost:8000")

        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id("id_new_item")

        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        inputbox.send_keys("Купить павлиньи перья")
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)

        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertTrue(any(rows.text == "1: Купить павлиньи перья" for row in rows), "Новый элемент списка не появился в таблице.")

        self.fail("Закончить тест ...")


if __name__ == "__main__":
    unittest.main(warnings='ignore')
