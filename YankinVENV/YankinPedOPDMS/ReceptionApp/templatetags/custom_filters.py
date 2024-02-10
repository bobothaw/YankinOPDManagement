from django import template
from datetime import datetime, date

register = template.Library()

@register.filter
def calculate_age(birth_date):
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

@register.filter
def date_since(value):
    if isinstance(value, date):
        delta = date.today() - value
        return delta.days
    return None
