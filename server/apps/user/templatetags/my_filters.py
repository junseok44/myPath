from django import template
from urllib.parse import urlparse

register = template.Library()

@register.filter
def add_protocol(link):
    parsed_url = urlparse(link)
    print(parsed_url.scheme)
    if not parsed_url.scheme:
        return f'http://{link}'
    return link


