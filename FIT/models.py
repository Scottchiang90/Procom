from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from FIT import UNIT_CHOICES


class Person(models.Model):
    name = models.CharField(max_length=50, verbose_name="full name")
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES)
    email = models.EmailField()
    mobile_number = PhoneNumberField(region='SG')

    class Meta:
        abstract = True


class Facilitator(Person):

    def __str__(self):
        return self.name


class Participant(Person):
    uid = models.CharField(max_length=20, verbose_name="Buddy FIT UID")
    nric = models.CharField(max_length=4, verbose_name="NRIC (Last 4 characters)")

    def __str__(self):
        return self.name


class Session(models.Model):
    capacity = models.IntegerField(default=40)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(default=60, verbose_name="duration (in mins)")
    conducting = models.ForeignKey(Facilitator, on_delete=models.PROTECT, related_name='conducting')
    safety = models.ForeignKey(Facilitator, on_delete=models.PROTECT, related_name='safety')
    call_link = models.URLField(blank=True)
    instructions = models.CharField(max_length=50, blank=True)
    participants = models.ManyToManyField(Participant, blank=True)

    def __str__(self):
        return "{date} {time}".format(date=self.date, time=self.time)
