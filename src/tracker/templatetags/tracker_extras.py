from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    """Remplace un paramètre d'URL sans dupliquer les autres."""
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()