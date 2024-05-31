import unittest

from html_classes.html import HtmlElement


class TestHtml(unittest.TestCase):

    def test_html(self):
        assert (HtmlElement(contents='test', css_classes='bs4', data_test='1').render()
                == '<div class="bs4" data-test="1">test</div>')

    def test_html_element(self):
        assert (HtmlElement(element='i', contents='test', css_classes='bs4', data_test='1').render()
                == '<i class="bs4" data-test="1">test</i>')

    def test_appending(self):
        html = HtmlElement(element='span', contents='line1')
        html.append('<br>line2')
        assert html.render() == '<span>line1<br>line2</span>'
