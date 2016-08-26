from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from genie.views import home_page

# Create your tests here.
class TestingHomepage(TestCase):
    def test_checking_homepage_uses_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)
    def test_checking_home_page_returns_home_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html")
        self.assertEqual(response.content.decode(),expected_html)
