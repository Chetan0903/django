from django import template
from django.contrib.auth.models import Group
register = template.Library()

@register.filter(name='isAdmin')
def isAdmin(user):
    return user.groups.filter(name='admin').exists() 