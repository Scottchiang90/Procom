from django.contrib import admin

from FIT.forms import AdminParticipationForm
from FIT.mixins import ExportCsvMixin
from FIT.models import Facilitator, Participant, Session, Participation


@admin.register(Facilitator)
class FacilitatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'email', 'mobile_number')
    search_fields = ('name', 'mobile_number',)
    list_filter = ('unit',)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'uid', 'nric', 'unit', 'email', 'mobile_number')
    search_fields = ('name', 'uid', 'nric',)
    list_filter = ('unit',)


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin, ExportCsvMixin):
    form = AdminParticipationForm
    list_display = ('session', 'participant', 'created_datetime')
    search_fields = ('session__date_time', 'participant__name')
    list_filter = ('session',)
    actions = ["export_as_csv"]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'duration', 'capacity', 'conducting', 'safety', 'call_link')
    search_fields = ('date_time', 'conducting__name')
