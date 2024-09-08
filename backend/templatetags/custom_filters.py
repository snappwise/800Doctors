from django import template

register = template.Library()


@register.filter
def range_filter(value):
    """Returns a range object as a list."""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)


# @register.filter(name='range_filter')
# def range_filter(value, arg=None):
#     """
#     Returns a range object as a list. Can be used as a replacement for range() in Jinja.
#     Usage in template: {{ some_value|range_filter:"end,step" }}
#     - If only value is provided, it acts as range(stop).
#     - If value and arg are provided, it acts as range(start, stop[, step]).
#     """
#     try:
#         if arg is None:
#             return range(int(value))

#         # Parse the arguments
#         parts = [int(x) for x in arg.split(',')]

#         if len(parts) == 1:
#             return range(int(value), parts[0])
#         elif len(parts) == 2:
#             return range(int(value), parts[0], parts[1])
#         else:
#             return range(0)
#     except (ValueError, TypeError):
#         return range(0)
