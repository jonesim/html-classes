# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`make-html` (PyPI package) — a Python library for building HTML programmatically using classes, with optional Bootstrap 4 and Font Awesome helpers. Django integration is optional; the library works standalone.

## Commands

**Run all tests:**
```bash
python -m pytest tests/
```

**Run a single test file:**
```bash
python -m pytest tests/test_html.py
```

**Run a single test:**
```bash
python -m pytest tests/test_html.py::TestHtml::test_html
```

**Build the package:**
```bash
python -m build
```

## Architecture

All core HTML generation lives in `html_classes/html.py`:

- **`HtmlElement`** — base class for all HTML elements. Renders `<element class="..." attr="...">contents</element>`. Key behaviours:
  - `kwargs` become HTML attributes; underscores are converted to hyphens (e.g. `data_test` → `data-test`)
  - `raw_attributes` dict bypasses underscore conversion
  - `default_classes`, `colour_class`, `default_colour` are class-level overrides used by subclasses
  - `end_tag=False` renders a self-closing tag (`<br/>`)
  - Contents can be a string, another `HtmlElement`, or a list of either; use `append()` or `+=` to add content
  - `__str__` calls `render()`, so elements can be embedded directly in f-strings or other elements
- **`HtmlTable`** — extends `HtmlElement` with `data` (list of rows/lists), `headers` (int: number of header rows), `left_headers`, `col_widths`, `col_styles`, `col_classes`, `grouped` (wraps in `<thead>`/`<tbody>`). Rows can be plain lists, `HtmlTr`, or mixed with `HtmlTd`/`HtmlTh` instances. Setting `col_widths` silently forces `grouped=True` and injects `style="table-layout: fixed; width: 100%;"` on the table element.
- **`HtmlRoot`** — a wrapper with no outer tag; renders its children concatenated. Useful as a document fragment.

`HtmlElement` also accepts a `tooltip` kwarg that injects Bootstrap tooltip data attributes (`data-tooltip="tooltip"`, `data-original-title`, `data-html="true"`) — handled in `tool_tip()`, not in `convert_kwargs()`.

When adding CSS classes, there are two paths: `css_classes` at init (accepts a space-separated string or a list) and `add_class(classes)` (always a space-separated string, extends the list). Don't add a third variant.

`html_classes/__init__.py` is intentionally empty — imports must come from submodules directly (e.g. `from html_classes.html import HtmlElement`).

Submodules:
- `html_classes/bs4.py` — Bootstrap 4 components (`HtmlBadge`, `HtmlAlert`) with `colour_class` and `default_colour` wired up
- `html_classes/font_awesome.py` — `font_awesome(classes, library=None, **kwargs)` renders `<i class="...">`. When Django is installed, icon names can be aliased via `settings.FONT_AWESOME_LIBRARY` dict.
- `html_classes/basic.py` — small helpers (e.g. `html_i`)

Django's `mark_safe` is used if available; otherwise it's a no-op identity function.
