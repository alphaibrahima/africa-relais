from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def current_link_active(context, name):
    try:
        if context["request"].resolver_match.url_name == name:
            return "active"
    except Exception:
        return ""
