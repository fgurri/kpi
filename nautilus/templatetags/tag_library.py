from django import template
import nautilus.utils as u

register = template.Library()

@register.filter()
def to_int(value):
    return int(value)

@register.filter()
def to_yyyy_monthname(value):
    return u.yyyymmToMonthName(str(value))
