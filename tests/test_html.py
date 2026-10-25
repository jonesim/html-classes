import unittest

from html_classes.font_awesome import font_awesome
from html_classes.html import (
    HtmlElement, HtmlRoot,
    HtmlDiv, HtmlSpan, HtmlA, HtmlP,
    HtmlH1, HtmlH2, HtmlH3, HtmlH4, HtmlH5, HtmlH6,
    HtmlStrong, HtmlEm,
    HtmlUl, HtmlOl, HtmlLi,
    HtmlImg, HtmlHr, HtmlBr,
    HtmlForm, HtmlButton, HtmlLabel, HtmlInput,
    HtmlSelect, HtmlOption, HtmlTextarea,
    HtmlNav, HtmlHeader, HtmlFooter, HtmlSection, HtmlMain,
)


class TestHtmlElement(unittest.TestCase):

    def test_html(self):
        self.assertEqual(HtmlElement(contents='test', css_classes='bs4', data_test='1').render(),
                         '<div class="bs4" data-test="1">test</div>')

    def test_html_element(self):
        self.assertEqual(HtmlElement(element='i', contents='test', css_classes='bs4', data_test='1').render(),
                         '<i class="bs4" data-test="1">test</i>')

    def test_css_classes_as_list(self):
        self.assertEqual(HtmlElement(css_classes=['btn', 'btn-primary']).render(),
                         '<div class="btn btn-primary"></div>')

    def test_appending_string(self):
        html = HtmlElement(element='span', contents='line1')
        html.append('<br>line2')
        self.assertEqual(html.render(), '<span>line1<br>line2</span>')

    def test_nested_elements(self):
        html = HtmlElement(element='button',
                           contents=font_awesome('fas fa-building'),
                           css_classes='btn btn-sm btn-outline-dark')
        self.assertEqual(html.render(),
                         '<button class="btn btn-sm btn-outline-dark"><i class="fas fa-building"></i></button>')

    def test_self_closing(self):
        self.assertEqual(HtmlElement(element='img', src='1.png', css_classes='bs4', data_test='1', end_tag=False).render(),
                         '<img class="bs4" src="1.png" data-test="1"/>')

    def test_end_tag_false(self):
        self.assertEqual(HtmlElement(element='br', end_tag=False).render(), '<br/>')

    def test_append_elements(self):
        html = HtmlElement(element='span')
        html.append(HtmlElement(element='h1', contents='test'))
        html.append(HtmlElement(element='h2', contents='test2'))
        self.assertEqual(html.render(), '<span><h1>test</h1><h2>test2</h2></span>')

    def test_add_operator(self):
        html = HtmlElement(element='span')
        html += HtmlElement(element='h1', contents='test')
        self.assertEqual(html.render(), '<span><h1>test</h1></span>')

    def test_append_list(self):
        html = HtmlElement(element='ul')
        html.append([HtmlElement(element='li', contents='a'), HtmlElement(element='li', contents='b')])
        self.assertEqual(html.render(), '<ul><li>a</li><li>b</li></ul>')

    def test_str(self):
        self.assertEqual(str(HtmlElement(element='p', contents='hi')), '<p>hi</p>')

    def test_add_class(self):
        el = HtmlElement(css_classes='foo')
        el.add_class('bar baz')
        self.assertEqual(el.render(), '<div class="foo bar baz"></div>')

    def test_add_attribute(self):
        el = HtmlElement(element='span', contents='x')
        el.add_attribute('data-id', '42')
        self.assertEqual(el.render(), '<span data-id="42">x</span>')

    def test_add_attribute_no_value(self):
        el = HtmlElement(element='input', end_tag=False)
        el.add_attribute('disabled')
        self.assertEqual(el.render(), '<input disabled/>')

    def test_raw_attributes(self):
        el = HtmlElement(element='div', raw_attributes={'style': 'color: red;'})
        self.assertEqual(el.render(), '<div style="color: red;"></div>')

    def test_tooltip(self):
        el = HtmlElement(element='span', contents='?', tooltip='Help text')
        self.assertEqual(el.render(), '<span title="Help text" data-tooltip="tooltip">?</span>')

    def test_tooltip_matches_ecosystem_contract(self):
        """django-modals helper.attr() and django_menus MenuItem emit the same pair."""
        el = HtmlElement(element='span', contents='?', tooltip='Help text')
        self.assertIn('title="Help text"', el.render())
        self.assertIn('data-tooltip="tooltip"', el.render())

    def test_tooltip_drops_bootstrap4_internals(self):
        """data-original-title is a BS4 internal and breaks under BS5, which needs a real title."""
        rendered = HtmlElement(element='span', contents='?', tooltip='Help text').render()
        self.assertNotIn('data-original-title', rendered)
        self.assertNotIn('data-html', rendered)

    def test_tooltip_html_still_available_via_kwargs(self):
        el = HtmlElement(element='span', contents='?', tooltip='<b>Help</b>', data_bs_html='true')
        self.assertIn('data-bs-html="true"', el.render())

    def test_tooltip_placement_via_kwargs(self):
        el = HtmlElement(element='span', contents='?', tooltip='Help', data_placement='bottom')
        self.assertIn('data-placement="bottom"', el.render())

    def test_no_tooltip_leaves_attributes_alone(self):
        self.assertEqual(HtmlElement(element='span', contents='?').render(), '<span>?</span>')

    def test_tooltip_overrides_explicit_title(self):
        el = HtmlElement(element='span', contents='?', title='ignored', tooltip='Help text')
        self.assertEqual(el.render(), '<span title="Help text" data-tooltip="tooltip">?</span>')

    def test_colour(self):
        class ColouredEl(HtmlElement):
            colour_class = 'text-'
            default_colour = 'primary'
        self.assertEqual(ColouredEl(contents='hi').render(), '<div class="text-primary">hi</div>')
        self.assertEqual(ColouredEl(contents='hi', colour='danger').render(), '<div class="text-danger">hi</div>')

    def test_underscore_to_hyphen(self):
        self.assertEqual(HtmlElement(element='div', aria_label='close').render(),
                         '<div aria-label="close"></div>')

    def test_trailing_underscore_stripped(self):
        self.assertEqual(HtmlElement(element='div', for_='field').render(),
                         '<div for="field"></div>')

    def test_single_quote_attributes(self):
        self.assertEqual(HtmlElement(element='button', contents='Go', onclick='f("x")',
                                     single_quote=True).render(),
                         '<button onclick=\'f("x")\'>Go</button>')

    def test_single_quote_class_and_raw_attributes(self):
        self.assertEqual(HtmlElement(css_classes='btn', raw_attributes={'style': 'width: 1px;'},
                                     single_quote=True).render(),
                         "<div class='btn' style='width: 1px;'></div>")

    def test_default_double_quote_attributes(self):
        self.assertEqual(HtmlElement(element='button', contents='Go', data_test='1').render(),
                         '<button data-test="1">Go</button>')

    def test_colour_class_not_duplicated_on_repeated_render(self):
        class ColouredEl(HtmlElement):
            colour_class = 'text-'
            default_colour = 'primary'
        el = ColouredEl(contents='hi')
        self.assertEqual(el.render(), '<div class="text-primary">hi</div>')
        self.assertEqual(el.render(), '<div class="text-primary">hi</div>')
        self.assertEqual(el.render(), '<div class="text-primary">hi</div>')

    def test_colour_class_not_duplicated_when_nested(self):
        class ColouredEl(HtmlElement):
            colour_class = 'text-'
            default_colour = 'primary'
        outer = HtmlElement(contents=ColouredEl(contents='hi'))
        self.assertEqual(outer.render(), '<div><div class="text-primary">hi</div></div>')
        self.assertEqual(outer.render(), '<div><div class="text-primary">hi</div></div>')

    def test_css_classes_as_str_subclass(self):
        class SafeString(str):
            pass
        self.assertEqual(HtmlElement(css_classes=SafeString('btn btn-primary')).render(),
                         '<div class="btn btn-primary"></div>')

    def test_falsy_contents_rendered(self):
        self.assertEqual(HtmlElement(contents=0).render(), '<div>0</div>')
        self.assertEqual(HtmlElement(contents=False).render(), '<div>False</div>')
        self.assertEqual(HtmlElement(contents='').render(), '<div></div>')

    def test_no_contents_still_empty(self):
        self.assertEqual(HtmlElement().render(), '<div></div>')
        self.assertEqual(HtmlElement(contents=None).render(), '<div></div>')
        self.assertEqual(HtmlElement(element='br', end_tag=False).render(), '<br/>')


class TestHtmlRoot(unittest.TestCase):

    def test_add(self):
        root = HtmlRoot()
        root += HtmlElement(element='h1', contents='test')
        root += HtmlElement(element='h2', contents='test2')
        self.assertEqual(root.render(), '<h1>test</h1><h2>test2</h2>')

    def test_append(self):
        root = HtmlRoot()
        root.append(HtmlElement(element='p', contents='para'))
        self.assertEqual(root.render(), '<p>para</p>')

    def test_init_with_contents(self):
        root = HtmlRoot(contents=HtmlElement(element='p', contents='x'))
        self.assertEqual(root.render(), '<p>x</p>')

    def test_str(self):
        root = HtmlRoot(contents=HtmlElement(element='p', contents='x'))
        self.assertEqual(str(root.render()), '<p>x</p>')


class TestConvenienceElements(unittest.TestCase):

    def test_div(self):
        self.assertEqual(HtmlDiv(contents='hi').render(), '<div>hi</div>')

    def test_span(self):
        self.assertEqual(HtmlSpan(contents='hi').render(), '<span>hi</span>')

    def test_a(self):
        self.assertEqual(HtmlA(contents='link', href='/page').render(), '<a href="/page">link</a>')

    def test_p(self):
        self.assertEqual(HtmlP(contents='text').render(), '<p>text</p>')

    def test_headings(self):
        self.assertEqual(HtmlH1(contents='Title').render(), '<h1>Title</h1>')
        self.assertEqual(HtmlH2(contents='Title').render(), '<h2>Title</h2>')
        self.assertEqual(HtmlH3(contents='Title').render(), '<h3>Title</h3>')
        self.assertEqual(HtmlH4(contents='Title').render(), '<h4>Title</h4>')
        self.assertEqual(HtmlH5(contents='Title').render(), '<h5>Title</h5>')
        self.assertEqual(HtmlH6(contents='Title').render(), '<h6>Title</h6>')

    def test_strong(self):
        self.assertEqual(HtmlStrong(contents='bold').render(), '<strong>bold</strong>')

    def test_em(self):
        self.assertEqual(HtmlEm(contents='italic').render(), '<em>italic</em>')

    def test_ul_ol_li(self):
        ul = HtmlUl()
        ul += HtmlLi(contents='a')
        ul += HtmlLi(contents='b')
        self.assertEqual(ul.render(), '<ul><li>a</li><li>b</li></ul>')

        ol = HtmlOl()
        ol += HtmlLi(contents='1')
        self.assertEqual(ol.render(), '<ol><li>1</li></ol>')

    def test_img(self):
        self.assertEqual(HtmlImg(src='a.png', alt='desc').render(), '<img src="a.png" alt="desc"/>')

    def test_hr(self):
        self.assertEqual(HtmlHr().render(), '<hr/>')

    def test_br(self):
        self.assertEqual(HtmlBr().render(), '<br/>')

    def test_form(self):
        self.assertEqual(HtmlForm(contents='x', method='post', action='/go').render(),
                         '<form method="post" action="/go">x</form>')

    def test_button(self):
        self.assertEqual(HtmlButton(contents='Go', css_classes='btn').render(),
                         '<button class="btn">Go</button>')

    def test_label(self):
        self.assertEqual(HtmlLabel(contents='Name', for_='f').render(), '<label for="f">Name</label>')

    def test_input(self):
        self.assertEqual(HtmlInput(type='text', name='q').render(), '<input type="text" name="q"/>')

    def test_select_and_option(self):
        sel = HtmlSelect(name='col')
        sel += HtmlOption(contents='Red', value='red')
        sel += HtmlOption(contents='Blue', value='blue')
        self.assertEqual(sel.render(),
                         '<select name="col"><option value="red">Red</option><option value="blue">Blue</option></select>')

    def test_textarea(self):
        self.assertEqual(HtmlTextarea(contents='', name='bio', rows='4').render(),
                         '<textarea name="bio" rows="4"></textarea>')

    def test_semantic_elements(self):
        self.assertEqual(HtmlNav(contents='x').render(), '<nav>x</nav>')
        self.assertEqual(HtmlHeader(contents='x').render(), '<header>x</header>')
        self.assertEqual(HtmlFooter(contents='x').render(), '<footer>x</footer>')
        self.assertEqual(HtmlSection(contents='x').render(), '<section>x</section>')
        self.assertEqual(HtmlMain(contents='x').render(), '<main>x</main>')
