from django.utils.html import escape
from django.utils.safestring import mark_safe


def build_link(href, text, cls=None, icon_class=None, **attrs):
    """Builds an html link.

    :param href: link for the anchor element
    :param text: text for the anchor element
    :param attrs: other attribute kwargs

    >>> link('xyz.com', 'hello', 'big')
    u'<a href="xyz.com" class="big">hello</a>'
    >>> link('xyz.com', 'hello', 'big', 'fa fa-times')
    u'<a href="xyz.com" class="big"><i class="fa fa-times"></i> hello</a>'
    """
    if not attrs:
        attrs = {}

    attrs['href'] = href

    if cls:
        attrs['class'] = cls

    attrs_formatted = u' '.join([u'{0}="{1}"'.format(k, v)
                                 for k, v in attrs.items()])

    icon = u'<i class="{0}"></i> '.format(icon_class) if icon_class else ''

    return mark_safe(u'<a {attrs}>{icon}{text}</a>'.format(
                                                    attrs=attrs_formatted,
                                                    icon=icon,
                                                    text=escape(text)))
