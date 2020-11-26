from django import template

register = template.Library()

@register.filter
def equal_channel(value, select_ch):
    return str(value)+"ch" == select_ch

@register.filter
def air_temp(value):
    return str(18+int(value)*2)

@register.filter
def just_temp(value,arg):
    return str(18+int(value)*2) == arg
