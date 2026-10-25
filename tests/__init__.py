"""Configure Django once for the whole suite, before any test module is imported.

Django is an optional dependency of make-html, so the suite must also pass without it —
tests that need Django skip via the ``django_required`` decorator below.
"""

try:
    from django.conf import settings
except ImportError:
    settings = None
else:
    if not settings.configured:
        settings.configure()

try:
    from django.test import override_settings
except ImportError:
    override_settings = None

import unittest

django_required = unittest.skipIf(settings is None, 'Django is not installed')
