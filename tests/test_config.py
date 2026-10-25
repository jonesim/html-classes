import unittest
from unittest import mock

from html_classes import config
from html_classes.config import (
    DEFAULT_FRAMEWORK, SUPPORTED_FRAMEWORKS, ImproperlyConfigured,
    get_css_framework, set_css_framework,
)

from . import django_required, override_settings


class TestFrameworkResolution(unittest.TestCase):

    def tearDown(self):
        set_css_framework(None)

    def test_default_is_bootstrap4(self):
        self.assertEqual(DEFAULT_FRAMEWORK, 'bootstrap4')
        self.assertEqual(get_css_framework(), 'bootstrap4')

    def test_supported_frameworks(self):
        self.assertEqual(SUPPORTED_FRAMEWORKS, ('bootstrap4', 'bootstrap5'))

    def test_set_css_framework(self):
        set_css_framework('bootstrap5')
        self.assertEqual(get_css_framework(), 'bootstrap5')
        set_css_framework('bootstrap4')
        self.assertEqual(get_css_framework(), 'bootstrap4')

    def test_set_css_framework_none_clears_override(self):
        set_css_framework('bootstrap5')
        set_css_framework(None)
        self.assertEqual(get_css_framework(), DEFAULT_FRAMEWORK)

    def test_set_css_framework_rejects_unknown(self):
        with self.assertRaises(ImproperlyConfigured):
            set_css_framework('bulma')
        self.assertEqual(get_css_framework(), DEFAULT_FRAMEWORK)


class TestDjangoSettings(unittest.TestCase):

    def tearDown(self):
        set_css_framework(None)

    @django_required
    def test_reads_css_framework_setting(self):
        with override_settings(CSS_FRAMEWORK='bootstrap5'):
            self.assertEqual(get_css_framework(), 'bootstrap5')

    @django_required
    def test_defaults_when_setting_absent(self):
        self.assertEqual(get_css_framework(), DEFAULT_FRAMEWORK)

    @django_required
    def test_override_beats_settings(self):
        set_css_framework('bootstrap4')
        with override_settings(CSS_FRAMEWORK='bootstrap5'):
            self.assertEqual(get_css_framework(), 'bootstrap4')

    @django_required
    def test_unknown_setting_raises(self):
        with mock.patch.object(config, '_delegate', None):
            with override_settings(CSS_FRAMEWORK='bulma'):
                with self.assertRaises(ImproperlyConfigured):
                    get_css_framework()


class TestAjaxHelpersDelegate(unittest.TestCase):
    """django-ajax-helpers >= 1.0.0 owns the setting; we defer to it when present."""

    def tearDown(self):
        set_css_framework(None)

    @django_required
    def test_delegate_used_when_available(self):
        delegate = mock.Mock(return_value='bootstrap5')
        with mock.patch.object(config, '_delegate', delegate):
            self.assertEqual(get_css_framework(), 'bootstrap5')
        delegate.assert_called_once_with()

    @django_required
    def test_local_fallback_used_when_delegate_absent(self):
        with mock.patch.object(config, '_delegate', None):
            with override_settings(CSS_FRAMEWORK='bootstrap5'):
                self.assertEqual(get_css_framework(), 'bootstrap5')

    def test_override_beats_delegate(self):
        delegate = mock.Mock(return_value='bootstrap5')
        with mock.patch.object(config, '_delegate', delegate):
            set_css_framework('bootstrap4')
            self.assertEqual(get_css_framework(), 'bootstrap4')
        delegate.assert_not_called()

    def test_delegate_not_consulted_without_configured_settings(self):
        """Standalone use must never reach ajax_helpers, which assumes Django settings."""
        delegate = mock.Mock(return_value='bootstrap5')
        with mock.patch.object(config, 'settings', None):
            with mock.patch.object(config, '_delegate', delegate):
                self.assertEqual(get_css_framework(), DEFAULT_FRAMEWORK)
        delegate.assert_not_called()
