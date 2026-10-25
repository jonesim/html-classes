"""CSS framework selection.

Delegates to django-ajax-helpers (>= 1.0.0) when it is installed, so the whole
ecosystem shares one implementation of the ``CSS_FRAMEWORK`` setting. Falls back
to an equivalent local implementation otherwise, keeping make-html usable
standalone and on older ajax-helpers releases.
"""

SUPPORTED_FRAMEWORKS = ('bootstrap4', 'bootstrap5')
DEFAULT_FRAMEWORK = 'bootstrap4'

try:
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    settings = None

    class ImproperlyConfigured(Exception):
        pass

try:
    # ajax-helpers < 1.0.0 has no config module, so ModuleNotFoundError is expected there
    from ajax_helpers.config import get_css_framework as _delegate
except ImportError:
    _delegate = None

_override = None


def validate_framework(framework):
    if framework not in SUPPORTED_FRAMEWORKS:
        raise ImproperlyConfigured(
            f"CSS_FRAMEWORK={framework!r} is not supported; choose one of {list(SUPPORTED_FRAMEWORKS)}")
    return framework


def set_css_framework(framework):
    """Select the framework without Django settings, for standalone use.

    Takes precedence over ``settings.CSS_FRAMEWORK`` so both paths behave alike.
    Pass ``None`` to clear the override.
    """
    global _override
    _override = None if framework is None else validate_framework(framework)


def get_css_framework():
    if _override is not None:
        return _override
    if settings is None or not settings.configured:
        return DEFAULT_FRAMEWORK
    if _delegate is not None:
        return _delegate()
    return validate_framework(getattr(settings, 'CSS_FRAMEWORK', DEFAULT_FRAMEWORK))
