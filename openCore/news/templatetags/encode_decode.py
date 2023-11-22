from django import template
from django.utils.safestring import mark_safe
import ftfy

register = template.Library()


@register.filter
def encode_decode(news_title):
    return ftfy.fix_text(news_title)
