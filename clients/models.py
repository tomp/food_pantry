from datetime import date
from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords


class Person(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    dob = models.DateField(help_text="Date of Birth", blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)

    @property
    def name(self) -> str:
        if self.last_name:
            return " ".join((self.first_name, self.last_name))
        return self.first_name

    @property
    def age(self) -> int:
        """The person's age in years."""
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    def __str__(self):
        return self.name


class Dependent(Person):
    dependent_on = models.ForeignKey('Client', related_name='dependents',
            on_delete=models.CASCADE,null=True)
    history = HistoricalRecords()


class Client(Person):
    NEW = 'NEW'
    TMP = 'TMP'
    APP = 'APP'
    REG = 'REG'
    STATUS_CHOICES = (
        (NEW, "New client"),
        (TMP, "Temp ID issued"),
        (APP, "Application submitted"),
        (REG, "Registered"))

    address = models.CharField(max_length=128, blank=True, null=True,
            help_text="Street Address")
    city = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, null=True)
    newId = models.CharField(max_length=32, blank=True, null=True)
    oldId = models.CharField(max_length=32, blank=True, null=True)
    tempId = models.CharField(max_length=32, blank=True, null=True)
    photo = models.ImageField(null=True)

    reg_notes = models.CharField(default="", max_length=256,
            blank=True, null=True, help_text="Registration notes")
    notes = models.CharField(default="", max_length=256,
            blank=True, null=True, help_text="General notes")
    history = HistoricalRecords()

    def id_number(self):
        if self.newId:
            return "#{}".format(self.newId)
        elif self.oldId:
            return "#{} (old)".format(self.oldId)
        elif self.tempId:
            return "temp #{}".format(self.tempId)
        return ""

    def last_visit(self):
        return self.visits.latest('visited_at').visited_at.date()

    def __str__(self):
        return "{} [{}]".format(self.name, self.id_number())

    class Meta:
        ordering = ['id']


class Visit(models.Model):
    client = models.ForeignKey('Client', related_name='visits')
    visited_at = models.DateTimeField(blank=True)
    picked_up_by = models.ForeignKey('Client', related_name='pickups', null=True)
    history = HistoricalRecords()

    def __str__(self):
        return "{} @ {}".format(str(self.client), self.visited_at.strftime("%Y-%m-%d"))

    class Meta:
        ordering = ['-visited_at', 'client']

