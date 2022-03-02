from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms import ModelForm, CharField, HiddenInput, TextInput

from FIT.models import Participation, Participant, Session


class ParticipateForm(ModelForm):
    uid = CharField(max_length=20, min_length=8, label="Buddy FIT UID")

    class Meta:
        model = Participation
        fields = ['session', 'participant']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "You have already signed up for this session.",
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['participant'].disabled = True
        self.fields['participant'].required = False
        self.fields['participant'].widget = HiddenInput()
        if kwargs['initial']:
            if kwargs['initial']['session']:
                self.fields['session'].disabled = True

    def clean_uid(self):
        return self.cleaned_data['uid'].upper()

    def clean(self):
        super().clean()
        participant, created = Participant.objects.get_or_create(
            uid=self.cleaned_data['uid']
        )
        self.cleaned_data['participant'] = participant
        this_session = self.cleaned_data['session']
        num_of_sign_ups = Participation.objects.filter(session=this_session).count()
        if num_of_sign_ups >= this_session.capacity:
            raise ValidationError('Sorry this session is fully booked.', code='exceed capacity')


class PostParticipateUpdateForm(ModelForm):

    class Meta:
        model = Participant
        fields = ['uid', 'name', 'unit', 'nric', 'email', 'mobile_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uid'].disabled = True
        self.fields['name'].required = True
        self.fields['unit'].required = True
        self.fields['nric'].required = True
        self.fields['email'].required = True


class AdminParticipationForm(ModelForm):

    class Meta:
        model = Participation
        fields = '__all__'
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "This participant have already signed up for this session.",
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        new_session = cleaned_data.get('session')
        # if update
        if self.instance.pk:
            # if session did not change
            if self.instance.session != new_session:
                check_capacity(new_session)
        # if create
        else:
            check_capacity(new_session)


def check_capacity(session):
    num_of_sign_ups = Participation.objects \
        .filter(session=session).count()
    if num_of_sign_ups >= session.capacity:
        raise ValidationError('Sorry this session is fully booked.', code='exceed capacity')