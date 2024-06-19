import unittest

from html_classes.html import HtmlTable, HtmlTr, HtmlTd


class TestTable(unittest.TestCase):

    def test_table(self):
        self.assertEqual(HtmlTable(data=[[1, 2],[3, 4]]).render(),
                         '<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>')


    def test_table_header(self):
        self.assertEqual(HtmlTable(data=[[1, 2],[3, 4]], headers=1).render(),
                         '<table><tr><th>1</th><th>2</th></tr><tr><td>3</td><td>4</td></tr></table>')

    def test_table_header_grouped(self):
        self.assertEqual(HtmlTable(data=[[1, 2],[3, 4]], headers=1, grouped=True).render(),
                         '<table><thead><tr><th>1</th><th>2</th></tr></thead>'
                         '<tbody><tr><td>3</td><td>4</td></tr></tbody></table>')

    def test_table_double_header_grouped(self):
        self.assertEqual(HtmlTable(data=[[1, 2],[3, 4]], headers=1, left_headers=1, grouped=True).render(),
                         '<table><thead><tr><th>1</th><th>2</th></tr></thead>'
                         '<tbody><tr><th>3</th><td>4</td></tr></tbody></table>')

    def test_table_html_row(self):
        self.assertEqual(HtmlTable(data=[HtmlTr(['1', '2']),[3, 4]],).render(),
                         '<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>')

    def test_table_html_td(self):
        self.assertEqual(HtmlTable(data=[['1', HtmlTd('2', css_classes='cls')],[3, 4]],).render(),
                         '<table><tr><td>1</td><td class="cls">2</td></tr><tr><td>3</td><td>4</td></tr></table>')
