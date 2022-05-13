from astro.models import Individual

from django import template
import urllib.parse

register = template.Library()

@register.simple_tag
def get_ind_user_id(user_id):
    return Individual.objects.get(user__id=user_id).id
