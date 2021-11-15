from django.db.models import Count, F
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from FIT.forms import ParticipateForm, PostParticipateUpdateForm
from FIT.models import Session, Participation, Participant


class SessionListView(ListView):
    model = Session
    queryset = Session.objects.filter(date_time__gt=timezone.now())\
        .annotate(available_count=F('capacity')-Count('participants'))\
        .order_by('date_time')
    context_object_name = 'sessions'

    def get_queryset(self):
        return Session.objects.filter(date_time__gt=timezone.now())\
            .annotate(available_count=F('capacity')-Count('participants'))\
            .order_by('date_time')


class ParticipateView(CreateView):
    model = Participation
    form_class = ParticipateForm
    session = None

    def get_session(self):
        if not self.session:
            self.session = Session.objects.get(id=self.kwargs['session_id'])
        return self.session

    def get_initial(self):
        initial = super().get_initial()
        initial['session'] = self.get_session()
        return initial

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['session'] = self.get_session()
        return context

    def get_success_url(self):
        if self.object.participant.name:
            return reverse_lazy('post-participate', args=(self.object.id,))
        return reverse_lazy('post-participate-update', args=(self.object.id,))


class PostParticipateDetailView(DetailView):
    model = Participant
    template_name = 'FIT/post_sign_up_detail.html'
    participation = None
    fields = '__all__'

    def get_object(self, queryset=None):
        if not self.participation:
            self.participation = Participation.objects.get(id=self.kwargs['participation_id'])
        self.kwargs[self.pk_url_kwarg] = self.participation.participant.id
        return super().get_object()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['session'] = self.participation.session
        context['participation'] = self.participation
        return context


class PostParticipateUpdateView(UpdateView):
    model = Participant
    template_name = 'FIT/post_sign_up_update.html'
    form_class = PostParticipateUpdateForm
    participation = None

    def get_object(self, queryset=None):
        if not self.participation:
            self.participation = Participation.objects.get(id=self.kwargs['participation_id'])
        self.kwargs[self.pk_url_kwarg] = self.participation.participant.id
        return super().get_object()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['session'] = self.participation.session
        return context

    def get_success_url(self):
        return reverse_lazy('post-participate', args=(self.participation.id,))
