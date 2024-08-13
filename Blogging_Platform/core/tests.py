from django.test import TestCase
from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from unittest.mock import patch

from core.views import home, article
from core.models import Posts

class HomeViewTestCase(TestCase):
    def test_home_view(self):
        request = HttpRequest()
        response = home(request)
        self.assertEqual(response.status_code, 200)

        
class ArticleViewTestCase(TestCase):
    def test_article_view_valid_slug(self):
        request = HttpRequest()
        response = article(request)
        self.assertEqual(response.status_code, 200)
        

    def test_article_view_invalid_slug(self):
        request = HttpRequest()
        response = article(request, article_slug='tle')
        self.assertEqual(response.status_code, 200)
        
        
    def test_article_view_exception_handling(self):        
        request = HttpRequest()
        response = article(request, article_id=1)
        self.assertEqual(response.status_code, 200)

