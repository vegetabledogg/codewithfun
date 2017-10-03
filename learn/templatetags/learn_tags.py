from django import template
from learn.models import Category

register = template.Library()

@register.assignment_tag
def get_all_categories():
    return Category.objects.all()
