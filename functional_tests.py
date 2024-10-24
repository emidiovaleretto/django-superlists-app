from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest
from time import sleep


class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        sleep(2)
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Liz has heard about a cool new to-do app.
        # She goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # then she notices the page title and header mention a to-do lists
        self.assertIn('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into the text field
        # Her hobby is tying fly-sishing lures
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and list the item
        # '1: Buy peacock feathers' as an item in her to-do list
        inputbox.send_keys(Keys.ENTER)
        sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_element_by_tag_name('tr')

        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            'New to-do item did not appear in table'
        )

        # There's still a text box invitting her to add another item.
        # Then she enters "Use peacock feathers to make a fly."
        self.fail('Finish the test!')

        # The page updates again and shows both items on her list

        # Liz wonders whether the site will remember her list.
        # Then she sees that the site has generate an unique URL for her
        # There is some explanatory text to that effect

        # She visits that URL - her to-do list is still there

        # Satisfied, she goes back to sleep


if __name__=='__main__':
    unittest.main()