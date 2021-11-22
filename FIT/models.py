from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from FIT import UNIT_CHOICES


class Person(models.Model):
    name = models.CharField(max_length=50, verbose_name="full name", blank=True)
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES, blank=True)
    email = models.EmailField(blank=True)
    mobile_number = PhoneNumberField(region='SG', blank=True)

    class Meta:
        abstract = True


class Facilitator(models.Model):
    name = models.CharField(max_length=50, verbose_name="full name")
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES)
    email = models.EmailField()
    mobile_number = PhoneNumberField(region='SG')

    def __str__(self):
        return self.name


class Participant(Person):
    uid = models.CharField(max_length=20, verbose_name="Buddy FIT UID", unique=True)
    nric = models.CharField(max_length=4, verbose_name="NRIC (Last 4 characters)", blank=True)

    def __str__(self):
        return self.name if self.name else self.uid


class Session(models.Model):
    capacity = models.IntegerField(default=40)
    date_time = models.DateTimeField()
    duration = models.IntegerField(default=60, verbose_name="duration (in mins)")
    conducting = models.ForeignKey(Facilitator, on_delete=models.PROTECT, related_name='conducting')
    safety = models.ForeignKey(Facilitator, on_delete=models.PROTECT, related_name='safety')
    call_link = models.URLField(blank=True)
    instructions = models.CharField(max_length=50, blank=True)
    participants = models.ManyToManyField(Participant, through='Participation', blank=True)

    def __str__(self):
        date_time_rep = self.date_time.astimezone(timezone.get_current_timezone()).strftime('%d/%m/%Y %H:%M')
        return "{date_time}-{conducting}".format(date_time=date_time_rep, conducting=self.conducting)


class Participation(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT)
    attended = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['session', 'participant']

    def __str__(self):
        return "{session}-{participant}".format(session=self.session, participant=self.participant)
