from django import template

register = template.Library()


@register.filter
def has_group(user, group_name):
    """
    Usage:
    {% if request.user|has_group:"Teacher" %}
    """
    if not user.is_authenticated:
        return False

    return user.groups.filter(name=group_name).exists()


@register.filter
def is_teacher(user):
    """
    Usage:
    {% if request.user|is_teacher %}
    """
    if not user.is_authenticated:
        return False

    return user.groups.filter(name="Teacher").exists()


@register.filter
def is_student(user):
    """
    Usage:
    {% if request.user|is_student %}
    """
    if not user.is_authenticated:
        return False

    return user.groups.filter(name="Student").exists()


@register.filter
def is_admin(user):
    """
    Usage:
    {% if request.user|is_admin %}
    """
    if not user.is_authenticated:
        return False

    return user.is_superuser or user.groups.filter(name="Admin").exists()