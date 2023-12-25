from urllib.parse import quote, unquote

import ftfy
from django import template

register = template.Library()


@register.filter
def encode_decode(news_title):
    return ftfy.fix_text(news_title)
