from datetime import date

from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords


class Person(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    dob = models.DateField(help_text="Date of Birth", blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    household = models.ForeignKey('Household', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return " ".join((self.firstname, self.lastname))


class Client(models.Model):
    NEW = 'NEW'
    TMP = 'TMP'
    APP = 'APP'
    REG = 'REG'
    STATUS_CHOICES = (
        (NEW, "New client"),
        (TMP, "Temp ID issued"),
        (APP, "Application submitted"),
        (REG, "Registered"))

    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, null=True)
    newId = models.CharField(max_length=32, blank=True, null=True)
    oldId = models.CharField(max_length=32, blank=True, null=True)
    tempId = models.CharField(max_length=32, blank=True, null=True)
    photo = models.ImageField(null=True)

    reg_notes = models.TextField(default="",
            blank=True, help_text="Registration notes")
    notes = models.TextField(default="",
            blank=True, help_text="General notes" )
    history = HistoricalRecords()

    def id_str(self):
        if self.newId:
            return "#" + self.newId
        elif self.oldId:
            return "({})".format(self.oldId)
        elif self.tempId:
            return "Temp #{}".format(self.tempId)
        else:
            return ""

    def __str__(self):
        return "{} ({})".format(str(self.person), self.id_str())


class Household(models.Model):
    address = models.CharField(max_length=128, blank=True, null=True,
            help_text="Street Address")
    city = models.CharField(max_length=64, blank=True, null=True)
    history = HistoricalRecords()


class Visit(models.Model):
    client = models.ForeignKey('Client')
    visited_at = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

    def __str__(self):
        return "{} @ {}".format(str(self.client), self.visited_at.strftime("%Y-%m-%d"))

