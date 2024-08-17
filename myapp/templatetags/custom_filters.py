# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})


@register.filter
def segundos_a_horas(segundos):
    if segundos is None:
        return 0
    horas = segundos / 3600
    return "{:.2f}".format(horas)