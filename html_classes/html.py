
try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = lambda a: a


class HtmlElement:
    element = 'div'
    default_classes = []
    colour_class = ''
    default_colour = None

    def convert_kwargs(self):
        if self.colour:
            self.css_classes.append(self.colour_class + self.colour)
        kwarg_str = '' if not self.css_classes else f' class="{" ".join(self.css_classes)}"'
        for k, v in self.attributes.items():
            kwarg_str += f' {k.replace("_", "-")}'
            if v is not None:
                kwarg_str += f'="{v}"'
        return kwarg_str

    def tool_tip(self, tooltip):
        if tooltip:
            self.attributes.update({'data-tooltip': "tooltip", 'data-original-title': tooltip, 'data-html': 'true'})

    def __init__(self, contents=None, css_classes=None, element=None, tooltip=None, colour=None, end=False,
                 void_tag=None, **kwargs):
        if element:
            self.element = element
        self._contents = contents if isinstance(contents, list) else ([contents] if contents else [])
        self.attributes = kwargs
        self.tool_tip(tooltip)
        self.colour = colour if colour else self.default_colour
        if css_classes:
            self.css_classes = css_classes.split(' ') if type(css_classes) == str else css_classes.copy()
        else:
            self.css_classes = self.default_classes.copy()
        self.void_tag = void_tag
        self.end = end

    def add_attribute(self, attr_name, attr_value=None):
        self.attributes[attr_name] = attr_value

    def get_contents(self):
        return ''.join([str(c) for c in self._contents])

    def render(self):
        if self.void_tag:
            if self.end:
                html = f'<{self.element}{self.convert_kwargs()}>{self.get_contents()}</{self.element}><{self.void_tag}>'
                return mark_safe(html)
            else:
                html = f'<{self.void_tag}><{self.element}{self.convert_kwargs()}>{self.get_contents()}</{self.element}>'
                return mark_safe(html)
        else:
            return mark_safe(f'<{self.element}{self.convert_kwargs()}>{self.get_contents()}</{self.element}>')

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
        elements = []
        for d in data:
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


class HtmlTable(HtmlElement):

    element = 'table'

    def get_contents(self):
        if self.headers:
            header_rows = []
            for i in self.rows[:self.headers]:
                header_rows.append(self.add_multiple_elements(i, 'th', css_classes=self.header_classes))
            header = self.add_multiple_elements(header_rows, 'tr')
            if self.grouped:
                header = HtmlElement(element='thead', contents=header).render()
        else:
            header = ''
        body_rows = []
        for r in self.rows[self.headers:]:
            body_rows.append(self.add_multiple_elements(r[:self.left_headers], 'th', css_classes=self.header_classes) +
                             self.add_multiple_elements(r[self.left_headers:], 'td', css_classes=self.cell_classes))
        body = self.add_multiple_elements(body_rows, 'tr')
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
