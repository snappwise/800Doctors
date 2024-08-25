from django import template

register = template.Library()


@register.filter
def range_filter(value):
    """Returns a range object as a list."""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)
