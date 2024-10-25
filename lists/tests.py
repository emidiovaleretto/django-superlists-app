from django.test import TestCase

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        request = self.client.get('/')
        self.assertTemplateUsed(request, 'home.html')