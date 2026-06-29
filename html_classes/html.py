
try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = lambda a: a


class HtmlElement:
    element = 'div'
    default_classes = []
    colour_class = ''
    default_colour = None
    end_tag = True
    single_quote = False

    def convert_kwargs(self):
        if self.colour:
            self.css_classes.append(self.colour_class + self.colour)
        q = "'" if self.single_quote else '"'
        kwarg_str = '' if not self.css_classes else f' class={q}{" ".join(self.css_classes)}{q}'
        for k, v in self.attributes.items():
            kwarg_str += f' {k.rstrip("_").replace("_", "-")}'
            if v is not None:
                kwarg_str += f'={q}{v}{q}'
        if self.raw_attributes:
            for k, v in self.raw_attributes.items():
                kwarg_str += f' {k}={q}{v}{q}'
        return kwarg_str

    def tool_tip(self, tooltip):
        if tooltip:
            self.attributes.update({'data-tooltip': "tooltip", 'data-original-title': tooltip, 'data-html': 'true'})

    def __init__(self, contents=None, css_classes=None, element=None, tooltip=None, colour=None, end_tag=None,
                 raw_attributes=None, single_quote=None, **kwargs):
        if element:
            self.element = element
        if single_quote is not None:
            self.single_quote = single_quote
        self._contents = contents if isinstance(contents, list) else ([contents] if contents else [])
        self.attributes = kwargs
        self.tool_tip(tooltip)
        self.raw_attributes = raw_attributes
        self.colour = colour if colour else self.default_colour
        if css_classes:
            self.css_classes = css_classes.split(' ') if type(css_classes) == str else css_classes.copy()
        else:
            self.css_classes = self.default_classes.copy()
        if end_tag is not None:
            self.end_tag = end_tag

    def add_attribute(self, attr_name, attr_value=None):
        self.attributes[attr_name] = attr_value

    def get_contents(self):
        return ''.join([str(c) for c in self._contents])

    def render(self):
        contents = self.get_contents()
        if len(contents) > 0 or self.end_tag:
            return mark_safe(f'<{self.element}{self.convert_kwargs()}>{contents}</{self.element}>')
        else:
            return mark_safe(f'<{self.element}{self.convert_kwargs()}/>')

    def append(self, additional_contents):
        if isinstance(additional_contents, list):
            self._contents += additional_contents
        else:
            self._contents.append(additional_contents)

    def add_class(self, classes):
        self.css_classes += classes.split(' ')

    def __str__(self):
        return self.render()

    def __add__(self, additional_contents):
        self.append(additional_contents)
        return self

    @staticmethod
    def add_multiple_elements(data, element, **kwargs):
        if isinstance(data, HtmlElement):
            return data.render()
        elements = []
        for d in data:
            if isinstance(d, HtmlElement):
                elements.append(d.render())
            else:
                elements.append(HtmlElement(element=element, contents=str(d), **kwargs).render())
        return ''.join(elements)


class HtmlDiv(HtmlElement):
    pass


class HtmlSpan(HtmlElement):
    element = 'span'


class HtmlA(HtmlElement):
    element = 'a'


class HtmlP(HtmlElement):
    element = 'p'


class HtmlH1(HtmlElement):
    element = 'h1'


class HtmlH2(HtmlElement):
    element = 'h2'


class HtmlH3(HtmlElement):
    element = 'h3'


class HtmlH4(HtmlElement):
    element = 'h4'


class HtmlH5(HtmlElement):
    element = 'h5'


class HtmlH6(HtmlElement):
    element = 'h6'


class HtmlStrong(HtmlElement):
    element = 'strong'


class HtmlEm(HtmlElement):
    element = 'em'


class HtmlUl(HtmlElement):
    element = 'ul'


class HtmlOl(HtmlElement):
    element = 'ol'


class HtmlLi(HtmlElement):
    element = 'li'


class HtmlImg(HtmlElement):
    element = 'img'
    end_tag = False


class HtmlHr(HtmlElement):
    element = 'hr'
    end_tag = False


class HtmlBr(HtmlElement):
    element = 'br'
    end_tag = False


class HtmlForm(HtmlElement):
    element = 'form'


class HtmlSelect(HtmlElement):
    element = 'select'


class HtmlOption(HtmlElement):
    element = 'option'


class HtmlTextarea(HtmlElement):
    element = 'textarea'


class HtmlNav(HtmlElement):
    element = 'nav'


class HtmlHeader(HtmlElement):
    element = 'header'


class HtmlFooter(HtmlElement):
    element = 'footer'


class HtmlSection(HtmlElement):
    element = 'section'


class HtmlMain(HtmlElement):
    element = 'main'


class HtmlButton(HtmlElement):
    element = 'button'


class HtmlLabel(HtmlElement):
    element = 'label'


class HtmlInput(HtmlElement):
    element = 'input'
    end_tag = False


class HtmlTh(HtmlElement):
    element = 'th'


class HtmlTd(HtmlElement):
    element = 'td'


class HtmlTr(HtmlElement):
    element = 'tr'

    def __init__(self, row_data=None, cell_classes=None, **kwargs):
        super().__init__(**kwargs)
        self.row_data = row_data
        self.cell_classes = cell_classes

    def get_contents(self):
        if self.row_data:
            return self.add_multiple_elements(self.row_data, 'td', css_classes=self.cell_classes)
        return ''.join([str(c) for c in self._contents])


class HtmlTable(HtmlElement):

    element = 'table'

    def _render_cells(self, row_data, element, base_classes=None):
        if not self.col_styles and not self.col_classes:
            return self.add_multiple_elements(row_data, element, css_classes=base_classes)
        cells = []
        for i, cell in enumerate(row_data):
            if isinstance(cell, HtmlElement):
                cells.append(cell.render())
            else:
                col_style = self.col_styles[i] if self.col_styles and i < len(self.col_styles) else None
                col_cls = self.col_classes[i] if self.col_classes and i < len(self.col_classes) else None
                classes = ' '.join(filter(None, [base_classes, col_cls])) or None
                raw_attrs = {'style': col_style} if col_style else None
                cells.append(HtmlElement(element=element, contents=str(cell),
                                         css_classes=classes, raw_attributes=raw_attrs).render())
        return ''.join(cells)

    def _render_body_rows(self):
        body_rows = []
        for r in self.rows[self.headers:]:
            if isinstance(r, HtmlTr):
                body_rows.append(r)
            else:
                body_rows.append(
                    self.add_multiple_elements(r[:self.left_headers], 'th', css_classes=self.header_classes) +
                    self._render_cells(r[self.left_headers:], 'td', base_classes=self.cell_classes)
                )
        return self.add_multiple_elements(body_rows, 'tr', css_classes=self.row_classes)

    def get_contents(self):
        colgroup = ''
        if self.col_widths:
            cols = ''.join(f'<col style="width: {w};">' for w in self.col_widths)
            colgroup = f'<colgroup>{cols}</colgroup>'

        if self.headers:
            header_rows = []
            for i in self.rows[:self.headers]:
                if isinstance(i, HtmlTr):
                    header_rows.append(i)
                else:
                    header_rows.append(self._render_cells(i, 'th', base_classes=self.header_classes))
            header = self.add_multiple_elements(header_rows, 'tr')
            if self.grouped:
                header = HtmlElement(element='thead', contents=header).render()
        else:
            header = ''

        body = self._render_body_rows()
        if self.grouped:
            body = HtmlElement(element='tbody', contents=body).render()

        return colgroup + header + body

    def render_body_rows(self):
        return mark_safe(self._render_body_rows())

    def render_row(self, index):
        r = self.rows[self.headers:][index]
        if isinstance(r, HtmlTr):
            return mark_safe(r.render())
        cells_html = (
            self.add_multiple_elements(r[:self.left_headers], 'th', css_classes=self.header_classes) +
            self._render_cells(r[self.left_headers:], 'td', base_classes=self.cell_classes)
        )
        return mark_safe(self.add_multiple_elements([cells_html], 'tr', css_classes=self.row_classes))

    def __init__(self, data=None, headers=0, left_headers=0, cell_classes=None, header_classes=None, row_classes=None,
                 grouped=False, col_widths=None, col_styles=None, col_classes=None, **kwargs):
        if col_widths and 'raw_attributes' not in kwargs:
            kwargs['raw_attributes'] = {'style': 'table-layout: fixed; width: 100%;'}
        super().__init__(**kwargs)
        self._data = data
        self.grouped = grouped or bool(col_widths)
        self.headers = headers
        self.left_headers = left_headers
        self.rows = [] if not data else [r for r in data]
        self.cell_classes = cell_classes
        self.header_classes = header_classes
        self.row_classes = row_classes
        self.col_widths = col_widths
        self.col_styles = col_styles
        self.col_classes = col_classes


class HtmlRoot:
    def __init__(self, contents=None):
        self._contents = contents if isinstance(contents, list) else ([contents] if contents else [])

    def get_contents(self):
        return ''.join([str(c) for c in self._contents])

    def render(self):
        return mark_safe(self.get_contents())

    def append(self, additional_contents):
        if isinstance(additional_contents, list):
            self._contents += additional_contents
        else:
            self._contents.append(additional_contents)

    def __add__(self, additional_contents):
        self.append(additional_contents)
        return self
