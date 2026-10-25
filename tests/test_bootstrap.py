import unittest

from html_classes.bootstrap import HtmlBadge, HtmlAlert
from html_classes.config import set_css_framework

from . import django_required, override_settings


class TestBootstrap4(unittest.TestCase):
    """bootstrap4 is the default, so these run with no framework configured at all."""

    def test_badge_default(self):
        self.assertEqual(HtmlBadge(contents='New').render(), '<span class="badge badge-primary">New</span>')

    def test_badge_colour(self):
        self.assertEqual(HtmlBadge(contents='Warn', colour='warning').render(),
                         '<span class="badge badge-warning">Warn</span>')

    def test_alert_default(self):
        self.assertEqual(HtmlAlert(contents='Info').render(), '<div class="alert alert-primary">Info</div>')

    def test_alert_colour(self):
        self.assertEqual(HtmlAlert(contents='Done', colour='success').render(),
                         '<div class="alert alert-success">Done</div>')


class TestBootstrap5(unittest.TestCase):

    def tearDown(self):
        set_css_framework(None)

    def test_badge_uses_text_bg_prefix(self):
        set_css_framework('bootstrap5')
        self.assertEqual(HtmlBadge(contents='New').render(), '<span class="badge text-bg-primary">New</span>')
        self.assertEqual(HtmlBadge(contents='Warn', colour='warning').render(),
                         '<span class="badge text-bg-warning">Warn</span>')

    def test_alert_unchanged(self):
        set_css_framework('bootstrap5')
        self.assertEqual(HtmlAlert(contents='Done', colour='success').render(),
                         '<div class="alert alert-success">Done</div>')

    def test_framework_read_at_render_time(self):
        badge = HtmlBadge(contents='New')
        self.assertEqual(badge.render(), '<span class="badge badge-primary">New</span>')
        set_css_framework('bootstrap5')
        self.assertEqual(badge.render(), '<span class="badge text-bg-primary">New</span>')
        set_css_framework('bootstrap4')
        self.assertEqual(badge.render(), '<span class="badge badge-primary">New</span>')

    @django_required
    def test_badge_follows_css_framework_setting(self):
        with override_settings(CSS_FRAMEWORK='bootstrap5'):
            self.assertEqual(HtmlBadge(contents='New').render(), '<span class="badge text-bg-primary">New</span>')
        self.assertEqual(HtmlBadge(contents='New').render(), '<span class="badge badge-primary">New</span>')


class TestColourClassDict(unittest.TestCase):
    """colour_class accepts a plain prefix or a dict keyed by framework."""

    def tearDown(self):
        set_css_framework(None)

    def test_string_colour_class_still_works(self):
        from html_classes.html import HtmlElement

        class Coloured(HtmlElement):
            colour_class = 'text-'
            default_colour = 'primary'

        set_css_framework('bootstrap5')
        self.assertEqual(Coloured().render(), '<div class="text-primary"></div>')

    def test_subclass_can_override_with_plain_string(self):
        class Bs4OnlyBadge(HtmlBadge):
            colour_class = 'badge-'

        set_css_framework('bootstrap5')
        self.assertEqual(Bs4OnlyBadge(contents='New').render(), '<span class="badge badge-primary">New</span>')
