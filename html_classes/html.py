
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

    def convert_kwargs(self):
        if self.colour:
            self.css_classes.append(self.colour_class + self.colour)
        kwarg_str = '' if not self.css_classes else f' class="{" ".join(self.css_classes)}"'
        for k, v in self.attributes.items():
            kwarg_str += f' {k.replace("_", "-")}'
            if v is not None:
                kwarg_str += f'="{v}"'
        if self.raw_attributes:
            for k, v in self.raw_attributes.items():
                kwarg_str += f' {k}="{v}"'
        return kwarg_str

    def tool_tip(self, tooltip):
        if tooltip:
            self.attributes.update({'data-tooltip': "tooltip", 'data-original-title': tooltip, 'data-html': 'true'})

    def __init__(self, contents=None, css_classes=None, element=None, tooltip=None, colour=None, end_tag=None,
                 raw_attributes=None, **kwargs):
        if element:
            self.element = element
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

    def get_contents(self):
        if self.headers:
            header_rows = []
            for i in self.rows[:self.headers]:
                if isinstance(i, HtmlTr):
                    header_rows.append(i)
                else:
                    header_rows.append(self.add_multiple_elements(i, 'th', css_classes=self.header_classes))
            header = self.add_multiple_elements(header_rows, 'tr')
            if self.grouped:
                header = HtmlElement(element='thead', contents=header).render()
        else:
            header = ''
        body_rows = []
        for r in self.rows[self.headers:]:
            if isinstance(r, HtmlTr):
                body_rows.append(r)
            else:
                body_rows.append(self.add_multiple_elements(r[:self.left_headers], 'th', css_classes=self.header_classes) +
                             self.add_multiple_elements(r[self.left_headers:], 'td', css_classes=self.cell_classes))
        body = self.add_multiple_elements(body_rows, 'tr' , css_classes=self.row_classes)
        if self.grouped:
            body = HtmlElement(element='tbody', contents=body).render()
        return header + body

    def __init__(self, data=None, headers=0, left_headers=0, cell_classes=None, header_classes=None, row_classes=None,
                 grouped=False, **kwargs):
        super().__init__(**kwargs)
        self._data = data
        self.grouped = grouped
        self.headers = headers
        self.left_headers = left_headers
        self.rows = [] if not data else [r for r in data]
        self.cell_classes = cell_classes
        self.header_classes = header_classes
        self.row_classes = row_classes


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
