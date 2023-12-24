from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def star_rating(value):
    return format_html('<span class="star-rating">{}</span>', '⭐' * value)
