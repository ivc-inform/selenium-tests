from unittest import skip

from selenium import webdriver

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

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
        self.assertNotIn(self.toDoList[0], page_text)
        self.assertNotIn(self.toDoList[1], page_text)

        self.imputToDo(self.toDoList[2])
        self.checkRowInToDoTabel(f"1: {self.toDoList[2]}")

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn(self.toDoList[0], page_text)
        self.assertIn(self.toDoList[2], page_text)

