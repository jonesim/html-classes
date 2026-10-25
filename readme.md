[![PyPI version](https://badge.fury.io/py/make-html.svg)](https://badge.fury.io/py/make-html)

# make-html

Build HTML from Python classes. Includes helpers for Bootstrap (4 and 5) and Font Awesome. Django integration is optional — the library works standalone.

## Installation

```bash
pip install make-html
```

## Imports

All classes and helpers are available directly from the top-level package:

```python
from html_classes import HtmlElement, HtmlDiv, HtmlTable, HtmlBadge, font_awesome
```

Or import from submodules if preferred:

```python
from html_classes.html import HtmlElement
from html_classes.bootstrap import HtmlBadge, HtmlAlert
from html_classes.font_awesome import font_awesome
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

## Escaping

**Attribute values** (including `css_classes`, `raw_attributes` and `tooltip`) are escaped so they can never end the attribute early:

- the quote character is always escaped (`"` → `&quot;`, or `'` → `&#x27;` with `single_quote=True`)
- `&` → `&amp;`, unless the value is marked safe (e.g. already passed through Django's `escape()`), so pre-escaped values are not double-escaped
- `<` and `>` are left as they are — they are legal inside a quoted attribute, so an HTML tooltip still works

```python
HtmlA(href='/?a=1&b=2', title='Say "hi"').render()
# → <a href="/?a=1&amp;b=2" title="Say &quot;hi&quot;"></a>
```

**Contents** are inserted verbatim — not escaped. Under Django, `render()` returns a `mark_safe` string, so the template engine will not escape it either. Escape any untrusted contents before passing them in:

```python
from django.utils.html import escape

HtmlElement(element='a', href=user_supplied_url, contents=escape(user_supplied_text))
```

Attribute escaping only keeps the markup well-formed — it does not make an untrusted value safe to use as a URL (`javascript:` hrefs) or as event-handler code.

`single_quote=True` switches attribute quoting to `'`, so a value containing `"` (e.g. JSON in an `onclick`) is output without `&quot;` entities.

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

## Tooltips

```python
HtmlElement(element='span', contents='?', tooltip='Help text').render()
# → <span title="Help text" data-tooltip="tooltip">?</span>
```

`title` carries the text; `data-tooltip="tooltip"` is the hook your page initialises on:

```javascript
// Bootstrap 5
document.querySelectorAll('[data-tooltip="tooltip"]')
        .forEach(el => new bootstrap.Tooltip(el));

// Bootstrap 4
$('[data-tooltip="tooltip"]').tooltip();
```

This is the same pair django-nested-modals and django-tab-menus emit, so one initialiser covers all three. With no JS at all it degrades to a native browser tooltip.

Placement and other options go through normal kwargs (underscores become hyphens):

```python
HtmlElement(element='span', contents='?', tooltip='Help', data_placement='bottom')
# → <span data-placement="bottom" title="Help" data-tooltip="tooltip">?</span>

HtmlElement(element='span', contents='?', tooltip='<b>Help</b>', data_bs_html='true')  # BS5 HTML tooltip
```

`tooltip=` takes precedence over an explicit `title=` kwarg.

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

HtmlLabel(contents='Name', for_='name-input').render()
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

## Bootstrap components

```python
from html_classes.bootstrap import HtmlBadge, HtmlAlert

HtmlBadge(contents='New').render()
# → <span class="badge badge-primary">New</span>

HtmlBadge(contents='Warning', colour='warning').render()
# → <span class="badge badge-warning">Warning</span>

HtmlAlert(contents='Saved!', colour='success').render()
# → <div class="alert alert-success">Saved!</div>
```

### Choosing Bootstrap 4 or 5

Bootstrap 5 renamed the badge colour classes from `badge-{colour}` to `text-bg-{colour}`. `HtmlBadge` follows whichever framework is selected; `HtmlAlert` is unchanged between the two.

The default is `bootstrap4`, so existing code is unaffected.

**In Django**, set `CSS_FRAMEWORK` — the same setting django-ajax-helpers uses, so one value drives both:

```python
# settings.py
CSS_FRAMEWORK = 'bootstrap5'
```

**Standalone**, call `set_css_framework()`:

```python
from html_classes import set_css_framework, HtmlBadge

set_css_framework('bootstrap5')
HtmlBadge(contents='New').render()
# → <span class="badge text-bg-primary">New</span>
```

`set_css_framework()` takes precedence over the Django setting; pass `None` to clear it. An unsupported value raises `ImproperlyConfigured`. The framework is read at render time, so `override_settings` works in tests.

When django-ajax-helpers 1.0.0+ is installed, `get_css_framework()` defers to `ajax_helpers.config` so the ecosystem shares one implementation; otherwise an equivalent local implementation reads the same setting.

## Font Awesome

```python
from html_classes.font_awesome import font_awesome

font_awesome('fas fa-question')
# → <i class="fas fa-question"></i>
```

`font_awesome` returns the rendered string directly, not an `HtmlElement` instance.

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

`colour_class` can also be a dict keyed by CSS framework, for components whose class name changed between Bootstrap 4 and 5:

```python
class MyBadge(HtmlElement):
    element = 'span'
    default_classes = ['badge']
    colour_class = {'bootstrap4': 'badge-', 'bootstrap5': 'text-bg-'}
    default_colour = 'primary'
```

Override `get_colour_class()` if you need to resolve the prefix some other way.
