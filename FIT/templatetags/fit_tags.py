import datetime

from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def end_time(session):
    return session.date_time + datetime.timedelta(minutes=session.duration)


@register.filter
def show_call_link(session):
    # hide if session is more than an hour ago
    if timezone.now() > session.date_time + datetime.timedelta(hours=1):
        return False
    return True


@register.filter
def is_absent(session):
    # absent if session has passed and not attended
    if timezone.now() > session.date_time:
        return True
    return False
