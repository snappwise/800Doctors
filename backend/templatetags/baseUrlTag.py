from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_base_url():
    return settings.ALLOWED_HOSTS[1]