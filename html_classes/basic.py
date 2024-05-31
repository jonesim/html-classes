from .html import HtmlElement


def html_i(text, **kwargs):
    return HtmlElement(element='i', contents=text, **kwargs).render()
