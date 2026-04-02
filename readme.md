[![PyPI version](https://badge.fury.io/py/make-html.svg)](https://badge.fury.io/py/make-html)

# make-html

Build HTML from Python classes. Includes helpers for Bootstrap 4 and Font Awesome. Django integration is optional — the library works standalone.

## Installation

```bash
pip install make-html
```

## Basic usage

```python
from html_classes.html import HtmlElement

# Simple element
HtmlElement(contents='Hello', css_classes='my-class').render()
# → <div class="my-class">Hello</div>

# Change the tag
HtmlElement(element='span', contents='Hello').render()
# → <span>Hello</span>

# kwargs become HTML attributes; underscores convert to hyphens
HtmlElement(element='input', end_tag=False, type='text', data_value='1').render()
# → <input type="text" data-value="1"/>

# Self-closing tag
HtmlElement(element='br', end_tag=False).render()
# → <br/>
```

`__str__` calls `render()`, so elements can be used directly in f-strings or nested inside other elements.

## Building up content

```python
from html_classes.html import HtmlElement, HtmlRoot

# append() or += to add children
el = HtmlElement(element='ul')
el.append(HtmlElement(element='li', contents='Item 1'))
el += HtmlElement(element='li', contents='Item 2')
# → <ul><li>Item 1</li><li>Item 2</li></ul>

# HtmlRoot renders children with no wrapping tag
root = HtmlRoot()
root += HtmlElement(element='h1', contents='Title')
root += HtmlElement(element='p', contents='Body')
root.render()
# → <h1>Title</h1><p>Body</p>
```

## CSS classes

```python
# String or list at init time
HtmlElement(css_classes='btn btn-primary')
HtmlElement(css_classes=['btn', 'btn-primary'])

# Add classes after construction
el = HtmlElement()
el.add_class('extra-class another-class')
```

## Tooltips (Bootstrap)

```python
HtmlElement(element='span', contents='?', tooltip='Help text').render()
# → <span data-tooltip="tooltip" data-original-title="Help text" data-html="true">?</span>
```

## Convenience elements

Pre-built subclasses so you don't need to pass `element=` every time.

### Text and inline

```python
from html_classes.html import HtmlP, HtmlSpan, HtmlA, HtmlStrong, HtmlEm
from html_classes.html import HtmlH1, HtmlH2, HtmlH3, HtmlH4, HtmlH5, HtmlH6

HtmlP(contents='A paragraph.').render()
# → <p>A paragraph.</p>

HtmlSpan(contents='highlighted', css_classes='text-danger').render()
# → <span class="text-danger">highlighted</span>

HtmlA(contents='Click here', href='https://example.com').render()
# → <a href="https://example.com">Click here</a>

HtmlStrong(contents='Bold').render()
# → <strong>Bold</strong>

HtmlEm(contents='Italic').render()
# → <em>Italic</em>

HtmlH1(contents='Page title').render()
# → <h1>Page title</h1>
```

### Lists

```python
from html_classes.html import HtmlUl, HtmlOl, HtmlLi

ul = HtmlUl()
ul += HtmlLi(contents='First')
ul += HtmlLi(contents='Second')
ul.render()
# → <ul><li>First</li><li>Second</li></ul>
```

### Media and void elements

```python
from html_classes.html import HtmlImg, HtmlHr, HtmlBr

HtmlImg(src='photo.jpg', alt='A photo').render()
# → <img src="photo.jpg" alt="A photo"/>

HtmlHr().render()
# → <hr/>

HtmlBr().render()
# → <br/>
```

`HtmlImg`, `HtmlHr`, and `HtmlBr` have `end_tag = False` by default.

### Forms

```python
from html_classes.html import HtmlForm, HtmlButton, HtmlLabel, HtmlInput, HtmlSelect, HtmlOption, HtmlTextarea

HtmlForm(contents='...', method='post', action='/submit').render()
# → <form method="post" action="/submit">...</form>

HtmlButton(contents='Click me', css_classes='btn btn-primary').render()
# → <button class="btn btn-primary">Click me</button>

HtmlLabel(contents='Name', raw_attributes={'for': 'name-input'}).render()
# → <label for="name-input">Name</label>

HtmlInput(type='text', name='username').render()
# → <input type="text" name="username"/>

HtmlSelect(contents='...', name='colour').render()
# → <select name="colour">...</select>

HtmlOption(contents='Red', value='red').render()
# → <option value="red">Red</option>

HtmlTextarea(contents='', name='bio', rows='4').render()
# → <textarea name="bio" rows="4"></textarea>
```

`HtmlInput` has `end_tag = False` by default, so it always renders as a self-closing tag.

### Layout and semantic

```python
from html_classes.html import HtmlDiv, HtmlNav, HtmlHeader, HtmlFooter, HtmlSection, HtmlMain

HtmlNav(contents='...', css_classes='navbar').render()
# → <nav class="navbar">...</nav>

HtmlHeader(contents='...').render()
# → <header>...</header>

HtmlFooter(contents='...').render()
# → <footer>...</footer>

HtmlSection(contents='...').render()
# → <section>...</section>

HtmlMain(contents='...').render()
# → <main>...</main>

HtmlDiv(contents='Hello', css_classes='container').render()
# → <div class="container">Hello</div>
```

### Inline helpers

```python
from html_classes.basic import html_i

html_i('Some italic text')
# → <i>Some italic text</i>
```

Returns the rendered string directly (not an `HtmlElement` instance).

## Tables

```python
from html_classes.html import HtmlTable, HtmlTr, HtmlTd

# Basic table — data is a list of rows, each row a list of cells
HtmlTable(data=[[1, 2], [3, 4]]).render()
# → <table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>

# headers=N treats the first N rows as header rows (<th>)
HtmlTable(data=[['Name', 'Age'], ['Alice', 30]], headers=1).render()
# → <table><tr><th>Name</th><th>Age</th></tr><tr><td>Alice</td><td>30</td></tr></table>

# grouped=True wraps in <thead>/<tbody>
HtmlTable(data=[['Name', 'Age'], ['Alice', 30]], headers=1, grouped=True).render()
# → <table><thead><tr><th>Name</th><th>Age</th></tr></thead><tbody><tr><td>Alice</td><td>30</td></tr></tbody></table>

# left_headers=N treats the first N columns of body rows as <th>
HtmlTable(data=[['Name', 'Age'], ['Alice', 30]], headers=1, left_headers=1).render()
# → <table><tr><th>Name</th><th>Age</th></tr><tr><th>Alice</th><td>30</td></tr></table>
```

### Column widths, styles, and classes

```python
# col_widths sets fixed column widths and forces table-layout: fixed; width: 100%
HtmlTable(data=rows, headers=1, col_widths=['30%', '70%'])

# Per-column inline styles
HtmlTable(data=rows, col_styles=['text-align: right;', None])

# Per-column CSS classes
HtmlTable(data=rows, col_classes=['text-right', None])
```

### Mixing HtmlTr / HtmlTd / HtmlTh in table data

Individual rows and cells can be `HtmlTr` / `HtmlTd` / `HtmlTh` instances for fine-grained control:

```python
from html_classes.html import HtmlTr, HtmlTd, HtmlTh

# HtmlTr accepts a list of cell values and an optional cell_classes
HtmlTr(row_data=['a', 'b'], cell_classes='text-center').render()
# → <tr><td class="text-center">a</td><td class="text-center">b</td></tr>

# HtmlTd and HtmlTh work like HtmlElement with their tag pre-set
HtmlTd(contents='value', css_classes='highlight').render()
# → <td class="highlight">value</td>

HtmlTh(contents='Header').render()
# → <th>Header</th>

# Mix pre-built rows and cells with plain lists inside HtmlTable
HtmlTable(data=[
    HtmlTr(['a', 'b']),
    ['c', HtmlTd('d', css_classes='highlight')],
])
```

## Bootstrap 4 components

```python
from html_classes.bs4 import HtmlBadge, HtmlAlert

HtmlBadge(contents='New').render()
# → <span class="badge badge-primary">New</span>

HtmlBadge(contents='Warning', colour='warning').render()
# → <span class="badge badge-warning">Warning</span>

HtmlAlert(contents='Saved!', colour='success').render()
# → <div class="alert alert-success">Saved!</div>
```

## Font Awesome

```python
from html_classes.font_awesome import font_awesome

font_awesome('fas fa-question').render()
# → <i class="fas fa-question"></i>
```

### Icon aliasing (Django)

Define a `FONT_AWESOME_LIBRARY` dict in Django settings to map short names to icon classes:

```python
# settings.py
FONT_AWESOME_LIBRARY = {
    'edit': 'fas fa-pen',
    'delete': 'fas fa-trash',
}
```

```python
font_awesome('edit')  # → <i class="fas fa-pen"></i>
```

Or pass a library dict directly without Django:

```python
font_awesome('edit', library={'edit': 'fas fa-pen'})
```

Extra kwargs are passed through as HTML attributes (e.g. for tooltips):

```python
font_awesome('fas fa-info', tooltip='More info')
```

## Subclassing

Subclass `HtmlElement` to create reusable components with fixed defaults:

```python
from html_classes.html import HtmlElement

class MyButton(HtmlElement):
    element = 'button'
    default_classes = ['btn', 'btn-primary']
    colour_class = 'btn-'
    default_colour = 'primary'
```

- `default_classes` — CSS classes applied when none are provided at init
- `colour_class` — prefix prepended to the `colour` value to form a class (e.g. `colour_class='btn-'` + `colour='danger'` → `btn-danger`)
- `default_colour` — fallback colour when none is passed
