import unittest

from html_classes.html import HtmlTable, HtmlTr, HtmlTd, HtmlTh


class TestTable(unittest.TestCase):

    def test_table(self):
        self.assertEqual(HtmlTable(data=[[1, 2], [3, 4]]).render(),
                         '<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>')

    def test_table_header(self):
        self.assertEqual(HtmlTable(data=[[1, 2], [3, 4]], headers=1).render(),
                         '<table><tr><th>1</th><th>2</th></tr><tr><td>3</td><td>4</td></tr></table>')

    def test_table_header_grouped(self):
        self.assertEqual(HtmlTable(data=[[1, 2], [3, 4]], headers=1, grouped=True).render(),
                         '<table><thead><tr><th>1</th><th>2</th></tr></thead>'
                         '<tbody><tr><td>3</td><td>4</td></tr></tbody></table>')

    def test_table_double_header_grouped(self):
        self.assertEqual(HtmlTable(data=[[1, 2], [3, 4]], headers=1, left_headers=1, grouped=True).render(),
                         '<table><thead><tr><th>1</th><th>2</th></tr></thead>'
                         '<tbody><tr><th>3</th><td>4</td></tr></tbody></table>')

    def test_table_html_row(self):
        self.assertEqual(HtmlTable(data=[HtmlTr(['1', '2']), [3, 4]]).render(),
                         '<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>')

    def test_table_html_td(self):
        self.assertEqual(HtmlTable(data=[['1', HtmlTd('2', css_classes='cls')], [3, 4]]).render(),
                         '<table><tr><td>1</td><td class="cls">2</td></tr><tr><td>3</td><td>4</td></tr></table>')

    def test_table_cell_classes(self):
        self.assertEqual(HtmlTable(data=[[1, 2]], cell_classes='p-1').render(),
                         '<table><tr><td class="p-1">1</td><td class="p-1">2</td></tr></table>')

    def test_table_header_classes(self):
        self.assertEqual(HtmlTable(data=[['A', 'B'], [1, 2]], headers=1, header_classes='fw-bold').render(),
                         '<table><tr><th class="fw-bold">A</th><th class="fw-bold">B</th></tr>'
                         '<tr><td>1</td><td>2</td></tr></table>')

    def test_table_row_classes(self):
        self.assertEqual(HtmlTable(data=[[1, 2]], row_classes='table-row').render(),
                         '<table><tr class="table-row"><td>1</td><td>2</td></tr></table>')

    def test_col_widths_adds_colgroup(self):
        result = HtmlTable(data=[[1, 2]], col_widths=['40%', '60%']).render()
        self.assertIn('<colgroup><col style="width: 40%;"><col style="width: 60%;"></colgroup>', result)

    def test_col_widths_forces_fixed_layout(self):
        result = HtmlTable(data=[[1, 2]], col_widths=['50%', '50%']).render()
        self.assertIn('table-layout: fixed', result)

    def test_col_widths_forces_grouped(self):
        result = HtmlTable(data=[[1, 2], [3, 4]], headers=1, col_widths=['50%', '50%']).render()
        self.assertIn('<thead>', result)
        self.assertIn('<tbody>', result)

    def test_col_styles(self):
        result = HtmlTable(data=[[1, 2]], col_styles=['text-align: right;', None]).render()
        self.assertIn('<td style="text-align: right;">1</td>', result)
        self.assertIn('<td>2</td>', result)

    def test_col_classes(self):
        result = HtmlTable(data=[[1, 2]], col_classes=['text-right', None]).render()
        self.assertIn('<td class="text-right">1</td>', result)
        self.assertIn('<td>2</td>', result)

    def test_col_classes_combined_with_cell_classes(self):
        result = HtmlTable(data=[[1, 2]], col_classes=['extra', None], cell_classes='base').render()
        self.assertIn('<td class="base extra">1</td>', result)
        self.assertIn('<td class="base">2</td>', result)

    def test_htmltr_cell_classes(self):
        self.assertEqual(HtmlTr(row_data=['a', 'b'], cell_classes='c').render(),
                         '<tr><td class="c">a</td><td class="c">b</td></tr>')

    def test_htmltd(self):
        self.assertEqual(HtmlTd(contents='val', css_classes='cls').render(), '<td class="cls">val</td>')

    def test_htmlth(self):
        self.assertEqual(HtmlTh(contents='hdr').render(), '<th>hdr</th>')

    def test_empty_table(self):
        self.assertEqual(HtmlTable().render(), '<table></table>')
