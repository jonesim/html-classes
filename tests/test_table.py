import unittest

from html_classes.html import HtmlTable


class TestTable(unittest.TestCase):

    def test_table(self):
        self.assertEqual(HtmlTable(data=[[1,2],[3, 4]]).render(),
                '<table><tr></tr><tr><td>1</td><td>2</td></tr><tr></tr><tr><td>3</td><td>4</td></tr></table>')
