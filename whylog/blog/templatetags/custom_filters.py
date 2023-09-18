from django import template
from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def remove_img_tags(value):
    soup = BeautifulSoup(value, 'html.parser')
    for img_tag in soup.find_all('img'):
        img_tag.decompose()
    return str(soup)


@register.filter
def get_from_dict(dictionary, key):
    return dictionary.get(key, "")