from .html import HtmlElement


class HtmlBadge(HtmlElement):
    element = 'span'
    default_classes = ['badge']
    colour_class = {'bootstrap4': 'badge-', 'bootstrap5': 'text-bg-'}
    default_colour = 'primary'


class HtmlAlert(HtmlElement):
    default_classes = ['alert']
    colour_class = 'alert-'
    default_colour = 'primary'
