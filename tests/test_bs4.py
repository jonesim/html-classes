import unittest

from html_classes.bs4 import HtmlBadge, HtmlAlert


class TestBs4(unittest.TestCase):

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
