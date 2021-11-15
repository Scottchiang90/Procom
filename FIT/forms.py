from django.core.exceptions import NON_FIELD_ERRORS
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

    def clean(self):
        participant, created = Participant.objects.get_or_create(
            uid=self.cleaned_data['uid']
        )
        self.cleaned_data['participant'] = participant
        return super(ParticipateForm, self).clean()


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
