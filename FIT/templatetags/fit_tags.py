import datetime

from django import template

register = template.Library()


@register.filter
def end_time(session):
    return session.date_time + datetime.timedelta(minutes=session.duration)
