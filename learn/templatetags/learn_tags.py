from django import template
from learn.models import Category,HaveLearned,TriedCourse

register = template.Library()

@register.assignment_tag
def get_all_categories():
    return Category.objects.all()

@register.filter
def have_learned(user, lesson):
    if(HaveLearned.objects.filter(user=user, lesson=lesson)):
        return True
    else:
        return False
    
@register.filter
def enrolled(user, course):
    if(TriedCourse.objects.filter(user=user, course=course)):
        return True
    else:
        return False