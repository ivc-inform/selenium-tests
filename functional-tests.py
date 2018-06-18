from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        "Установка"
        self.browser = webdriver.Firefox()

    def tearDown(self):
        "Демонтаж"
        self.browser.quit()

    def test_all(self):
        self.browser.get("http://localhost:8000")

        self.assertIn('To-Do', self.browser.title)
        self.fail("Закончить тест ...")

if __name__=="__main__":
    unittest.main(warnings='ignore')