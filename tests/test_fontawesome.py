import unittest

from html_classes.font_awesome import font_awesome


class TestFontAwesome(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(font_awesome('fas fa-question'), '<i class="fas fa-question"></i>')

    def test_library_kwarg(self):
        lib = {'edit': 'fas fa-pen', 'delete': 'fas fa-trash'}
        self.assertEqual(font_awesome('edit', library=lib), '<i class="fas fa-pen"></i>')
        self.assertEqual(font_awesome('delete', library=lib), '<i class="fas fa-trash"></i>')

    def test_library_passthrough_unknown_key(self):
        lib = {'edit': 'fas fa-pen'}
        self.assertEqual(font_awesome('fas fa-star', library=lib), '<i class="fas fa-star"></i>')

    def test_kwargs_passthrough(self):
        result = font_awesome('fas fa-info', id='icon1')
        self.assertIn('id="icon1"', result)
        self.assertIn('class="fas fa-info"', result)

    def test_tooltip_passthrough(self):
        result = font_awesome('fas fa-info', tooltip='Help')
        self.assertIn('data-original-title="Help"', result)

    def test_django_settings(self):
        try:
            from django.conf import settings
            settings.configure(FONT_AWESOME_LIBRARY={'edit': 'fas fa-pen'})
        except ImportError:
            pass
        self.assertEqual(font_awesome('edit'), '<i class="fas fa-pen"></i>')
