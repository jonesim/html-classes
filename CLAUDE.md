# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`make-html` (PyPI package) — a Python library for building HTML programmatically using classes, with optional Bootstrap (4 and 5) and Font Awesome helpers. Django integration is optional; the library works standalone.

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

`tests/__init__.py` calls `settings.configure()` once, before any test module is imported — never call it again from inside a test (it raises if settings are already configured). Use `override_settings` instead. Django-dependent tests carry the `@django_required` decorator from the same module, so the suite still passes with Django uninstalled.

## Architecture

All core HTML generation lives in `html_classes/html.py`:

- **`HtmlElement`** — base class for all HTML elements. Renders `<element class="..." attr="...">contents</element>`. Key behaviours:
  - `kwargs` become HTML attributes; underscores are converted to hyphens (e.g. `data_test` → `data-test`)
  - `raw_attributes` dict bypasses underscore conversion
  - `default_classes`, `colour_class`, `default_colour` are class-level overrides used by subclasses
  - `colour_class` is either a prefix string or a dict keyed by CSS framework (`{'bootstrap4': 'badge-', 'bootstrap5': 'text-bg-'}`), resolved by `get_colour_class()` at render time
  - `end_tag=False` renders a self-closing tag (`<br/>`)
  - Contents can be a string, another `HtmlElement`, or a list of either; use `append()` or `+=` to add content
  - `__str__` calls `render()`, so elements can be embedded directly in f-strings or other elements
  - `render()` must stay side-effect free — an element can be rendered repeatedly (and is, whenever a parent re-renders). Build derived state (e.g. the `colour_class` + `colour` class) into a local, never onto `self.css_classes`.
  - Falsy contents (`0`, `''`, `False`) are kept; only `None` means "no contents"
- **`HtmlTable`** — extends `HtmlElement` with `data` (list of rows/lists), `headers` (int: number of header rows), `left_headers`, `col_widths`, `col_styles`, `col_classes`, `grouped` (wraps in `<thead>`/`<tbody>`). Rows can be plain lists, `HtmlTr`, or mixed with `HtmlTd`/`HtmlTh` instances. Setting `col_widths` silently forces `grouped=True` and injects `style="table-layout: fixed; width: 100%;"` on the table element, merging with any `raw_attributes` the caller supplied (a caller-supplied `style` is appended after the layout rules, so it wins on conflicting properties).
- **`HtmlRoot`** — a wrapper with no outer tag; renders its children concatenated. Useful as a document fragment.

`HtmlElement` also accepts a `tooltip` kwarg that emits `title="…"` plus `data-tooltip="tooltip"` — handled in `tool_tip()`, not in `convert_kwargs()`. That pair is the ecosystem's static tooltip contract, matching `django_modals.helper.attr()` and `django_menus` `MenuItem`; apps initialise on the `[data-tooltip="tooltip"]` selector. Don't add `data-original-title`/`data-html` back — they are Bootstrap 4 internals (BS5 uses `data-bs-*` and requires a real `title`). Placement and options ride on normal kwargs (`data_placement='bottom'`, `data_bs_html='true'`).

When adding CSS classes, there are two paths: `css_classes` at init (accepts a space-separated string or a list) and `add_class(classes)` (always a space-separated string, extends the list). Don't add a third variant.

`html_classes/__init__.py` re-exports the public API, so both `from html_classes import HtmlElement` and `from html_classes.html import HtmlElement` work. Keep the re-export list in sync when adding a public class.

Submodules:
- `html_classes/config.py` — `get_css_framework()` / `set_css_framework()`. Selects `'bootstrap4'` (default) or `'bootstrap5'`. Soft dependency: delegates to `ajax_helpers.config.get_css_framework` when django-ajax-helpers >= 1.0.0 is installed, otherwise reads the same `CSS_FRAMEWORK` Django setting itself. `set_css_framework()` is an in-process override for standalone (non-Django) use and beats the setting. Never resolve the framework at import time — always call `get_css_framework()` at render time so `override_settings` works.
- `html_classes/bootstrap.py` — Bootstrap components (`HtmlBadge`, `HtmlAlert`) with `colour_class` and `default_colour` wired up
- `html_classes/font_awesome.py` — `font_awesome(classes, library=None, **kwargs)` returns a rendered `<i class="...">` string, not an `HtmlElement`. When Django is installed, icon names can be aliased via `settings.FONT_AWESOME_LIBRARY` dict.

Django's `mark_safe` is used if available; otherwise it's a no-op identity function.

## jQuery removal & Bootstrap 5 support (July 2026)

Part of a cross-package migration (summary in `X:\CLAUDE.md`). This package has **no jQuery** — the work here is tiny but it is a **release blocker for django-modals**, which currently pins `make-html` to git SHA `f826007` because its new BS5 field renderer (`field_render.py`) and rewritten `helper.py` depend on unreleased html-classes code.

### To do
1. ~~**`HtmlBadge` colour prefix**~~ — done. `colour_class` is now `{'bootstrap4': 'badge-', 'bootstrap5': 'text-bg-'}`, resolved at render time by `HtmlElement.get_colour_class()` via `config.get_css_framework()`. `HtmlAlert` (`alert-*`) is unchanged in BS5, as expected. Selection follows the ecosystem `CSS_FRAMEWORK` setting, with `set_css_framework()` for standalone use — see `config.py` above.

   **Ecosystem inconsistency to resolve:** django-modals reads `MODALS_CSS_FRAMEWORK` (`field_render.py:205`), not `CSS_FRAMEWORK`. A project that sets only `MODALS_CSS_FRAMEWORK='bootstrap5'` gets BS5 modals but BS4 badges. django-modals should fall back to `CSS_FRAMEWORK`; make-html deliberately reads only `CSS_FRAMEWORK` and does not know about the modals setting.
2. ~~**Tooltip attributes**~~ — done. `tool_tip()` now emits `title` + `data-tooltip="tooltip"`.

   Worth recording, because the original note was based on a wrong assumption: ajax_helpers' rewritten `tooltip()` (`ajax_helpers.js:379`) is **only** for AJAX-populated tooltips via `{% tooltip_init selector function_name %}` — it reads `el.dataset`, POSTs it, and injects the response into `.ah-tooltip-inner`. It never reads `title`/`data-original-title`/`data-html`, and 1.0.0 ships **no static tooltip initialiser**. So there was no ajax_helpers contract to align with; the real contract is the one django-modals (`helper.py:51,125`) and django_menus (`menu_items.py:187`) already emit, with apps initialising on `[data-tooltip="tooltip"]`.

   The old output was also broken under BS5, not merely dated: `data-original-title` is a BS4 internal (BS5 uses `data-bs-original-title` and requires a real `title`), so a make-html tooltip rendered nothing under BS5 and had no native fallback.
3. ~~**Fix the SafeString bug**~~ — done. The fault was in `__init__`, not `render()`: `type(css_classes) == str` was `False` for `str` subclasses, so a Django `SafeString` fell through to `css_classes.copy()` and raised `AttributeError`. Since `render()` returns `mark_safe(...)`, feeding any rendered output (e.g. `font_awesome(...)`) back in as `css_classes` crashed. Now uses `isinstance`. **Still to do there:** remove the `fa_icon()` workaround from django-modals' `helper.py` once 1.0.0 is released.
4. **Release to PyPI** (1.0.0) once the above land — this unblocks the django-modals publish (its `publish.yml` is staged and must not run before `make-html` resolves from PyPI).

   1.0.0 rather than 0.0.4 because the tooltip change is **breaking**: `data-original-title`/`data-html` are gone, so any page relying on those attributes needs its tooltip init pointed at `title` + `data-tooltip="tooltip"`. It also lines up with django-ajax-helpers 1.0.0.

   After release, downstream pins need updating: django-modals' `requirements.txt` currently has `make-html @ git+https://github.com/jonesim/html-classes@f826007…` and its `pyproject.toml` has an unversioned `"make-html"` — both should become `make-html>=1.0.0`. `X:\financial\requirements.txt` also carries a git pin (`@b31665c…`).

## Releasing

Full process in `X:\CLAUDE.md` → "Releasing a package". Summary: once-over the diff since the last release tag (`git fetch --tags origin` first), bump `version` in `pyproject.toml`, commit, run `X:\release.bat` — it tags `v<version>` and pushes. `.github/workflows/publish.yml` runs the pytest suite first, then builds and publishes to PyPI via trusted publishing. First Actions release: confirm the GitHub `pypi` environment and the PyPI trusted publisher for `make-html` are configured. Releasing this package is the gate for the django-nested-modals release (see above).
