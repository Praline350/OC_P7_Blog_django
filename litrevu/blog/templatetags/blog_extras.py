from django.template import Library
from django.utils import timezone
from django.templatetags.static import static


MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = Library()


@register.simple_tag(takes_context=True)
def get_ticket_display(context, user):
    if context["user"] == user:
        return "Vous"
    return user.username


@register.filter
def get_time_display(time_created):
    seconds_ago = (timezone.now() - time_created).total_seconds()
    if seconds_ago <= HOUR:
        return f"Publié il y a {int(seconds_ago // MINUTE)} minutes."
    elif seconds_ago <= DAY:
        return f"Publié il y a {int(seconds_ago // HOUR)} heures."
    return f"Publié le {time_created.strftime('%d %B %Y à %Hh%M')}"


@register.filter
def profile_photo_or_default(user):
    if user.profile_photo:
        return user.profile_photo.url
    return static("images/default_profile.png")


@register.filter
def capitalize_first(value):
    """Capitalize the first letter of the value"""
    if not isinstance(value, str):
        return value
    return value.capitalize()
