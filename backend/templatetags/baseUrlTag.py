from django import template

register = template.Library()

@register.simple_tag
def get_base_url():
    return "http://127.0.0.1:8000"