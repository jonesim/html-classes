import unittest

from html_classes.font_awesome import font_awesome
from html_classes.html import HtmlElement, HtmlRoot


class TestHtml(unittest.TestCase):

    def test_html(self):
        self.assertEqual(HtmlElement(contents='test', css_classes='bs4', data_test='1').render(),
                         '<div class="bs4" data-test="1">test</div>')

    def test_html_element(self):
        self.assertEqual(HtmlElement(element='i', contents='test', css_classes='bs4', data_test='1').render(),
                         '<i class="bs4" data-test="1">test</i>')

    def test_appending(self):
        html = HtmlElement(element='span', contents='line1')
        html.append('<br>line2')
        self.assertEqual(html.render(), '<span>line1<br>line2</span>')

    def test_nested_elements(self):
        html = HtmlElement(element='button',
                           contents=font_awesome('fas fa-building'),
                           css_classes='btn btn-sm btn-outline-dark')
        expected_result = '<button class="btn btn-sm btn-outline-dark"><i class="fas fa-building"></i></button>'
        self.assertEqual(html.render(), expected_result)

    def test_image(self):
        self.assertEqual(HtmlElement(element='img', src='1.png', css_classes='bs4', data_test='1', end_tag=False).render(),
                         '<img class="bs4" src="1.png" data-test="1"/>')

    def test_append(self):
        html = HtmlElement(element='span')
        html.append(HtmlElement(element='h1', contents='test'))
        html.append(HtmlElement(element='h2', contents='test2'))

        expected_result = '<span><h1>test</h1><h2>test2</h2></span>'

        self.assertEqual(html.render(), expected_result)

    def test_add(self):
        root = HtmlRoot()
        root += HtmlElement(element='h1', contents='test')
        root += HtmlElement(element='h2', contents='test2')

        expected_result = '<h1>test</h1><h2>test2</h2>'

        self.assertEqual(root.render(), expected_result)

    def test_end_tag(self):
        html = HtmlElement(element='br', end_tag=False)
        self.assertEqual(html.render(), '<br/>')