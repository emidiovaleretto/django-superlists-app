from time import time, sleep
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10
class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        sleep(2)
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time() - start_time > MAX_WAIT:
                    raise e
                sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Liz has heard about a cool new to-do app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)

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
        inputbox.send_keys('Buy peacock feathers.')

        # When she hits enter, the page updates, and list the item
        # '1: Buy peacock feathers' as an item in her to-do list
        inputbox.send_keys(Keys.ENTER)
        sleep(1)
        self.wait_for_row_in_list_table('1: Buy peacock feathers.')

        # There's still a text box invitting her to add another item.
        # Then she enters "Use peacock feathers to make a fly."
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly.')
        inputbox.send_keys(Keys.ENTER)
        sleep(1)

        self.wait_for_row_in_list_table('1: Buy peacock feathers.')
        self.wait_for_row_in_list_table(
            '2: Use peacock feathers to make a fly.'
        )

        # The page updates again and shows both items on her list
        self.wait_for_row_in_list_table(
            '2: Use peacock feathers to make a fly.'
        )
        self.wait_for_row_in_list_table('1: Buy peacock feathers.')

        # Liz wonders whether the site will remember her list.
        # Then she sees that the site has generate an unique URL for her
        # There is some explanatory text to that effect

        # She visits that URL - her to-do list is still there

        # Satisfied, she goes back to sleep

        self.fail('Finish the test!')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Liz starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(
            '1: Buy peacock feathers'
        )

        # She notices that her list has a unique URL
        liz_list_url = self.browser.current_url
        self.assertRegex(liz_list_url, '/lists/.+')

        # Now a new user, Analu, comes along to the sute.
        ## We use a new browser to make sure that no information
        ## of Liz's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Analu visits the home page. There is no sign of Liz's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Analu starts a new list by entering a new item.
        # She's less interesting then Liz...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Analu gets her own unique URL
        analu_list_url = self.browser.current_url
        self.assertRegex(analu_list_url, '/lists/.+')
        # self.assertRedirects(
        # analu_list_url, 'lists/the-only-list-in-the-world/')
        self.assertNotEqual(liz_list_url, analu_list_url)

        # Again, there's no trace of Liz's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Buy peacock feathers', page_text)
        self.assertIn('1: Buy milk', page_text)
