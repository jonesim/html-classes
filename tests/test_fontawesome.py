import unittest

from html_classes.font_awesome import font_awesome


class TestFontAwesome(unittest.TestCase):

    def test_basic(self):
        self.assertEqual( font_awesome('fas fa-question'), '<i class="fas fa-question"></i>')

    def test_django_settings(self):
        try:
            from django.conf import settings
            settings.configure(FONT_AWESOME_LIBRARY={'edit': 'fas fa-pen'})
        except ImportError:
            pass
        self.assertEqual(font_awesome('edit'), '<i class="fas fa-pen"></i>')
