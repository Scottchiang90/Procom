from django.contrib import admin
from django.urls import path

from .views import SessionListView, ParticipateView, PostParticipateUpdateView, PostParticipateDetailView, MyParticipationListView

admin.site.site_header = 'PROCOM'                       # default: "Django Administration"
admin.site.index_title = 'PROCOM administration'        # default: "Site administration"
admin.site.site_title = 'PROCOM site admin'             # default: "Django site admin"

urlpatterns = [
    path('', SessionListView.as_view(), name='index'),
    path('participate/<int:session_id>/', ParticipateView.as_view(), name='participate'),
    path('participate-success/<int:participation_id>/', PostParticipateDetailView.as_view(), name='post-participate'),
    path('participate-update/<int:participation_id>/', PostParticipateUpdateView.as_view(), name='post-participate-update'),
    path('my-sessions/', MyParticipationListView.as_view(), name='my-sessions'),
]
