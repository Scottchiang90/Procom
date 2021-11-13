from django.views.generic import ListView

from FIT.models import Session


class SessionListView(ListView):
    model = Session
    template_name = "FIT/session_list.html"
    context_object_name = 'sessions'
