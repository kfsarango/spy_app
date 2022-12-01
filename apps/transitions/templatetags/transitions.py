from django import template

register = template.Library()


@register.simple_tag()
def get_meta_data(instance):
    return {
        "app_name": instance.__class__._meta.app_label,
        "model_name": instance.__class__._meta.model_name,
    }
