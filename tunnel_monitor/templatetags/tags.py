from django.template.defaulttags import register

# Credits to https://stackoverflow.com/a/8000091
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)