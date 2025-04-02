from .html import HtmlElement
try:
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    settings = None
    ImproperlyConfigured = None

def font_awesome(classes, library=None, **kwargs):
    if library is not None:
        classes = library.get(classes, classes)
    elif settings is not None:
        try:
            classes = getattr(settings, 'FONT_AWESOME_LIBRARY', {}).get(classes, classes)
        except ImproperlyConfigured:
            pass
    return HtmlElement(element='i', css_classes=classes, **kwargs).render()
