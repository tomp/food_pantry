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
    dob = models.DateField(help_text="Date of Birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    household = models.ForeignKey('Household', on_delete=models.CASCADE)
    history = HistoricalRecords()


class Client(models.Model):
    NEW = 'NEW'
    APP = 'APP'
    REG = 'REG'
    STATUS_CHOICES = (
        (NEW, "New client"),
        (APP, "Application submitted"),
        (REG, "Registered"))

    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    household = models.ForeignKey('Household', on_delete=models.CASCADE)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES)
    newId = models.IntegerField()
    oldId = models.IntegerField()
    photo = models.ImageField()
    notes = models.TextField()
    history = HistoricalRecords()


class Household(models.Model):
    address = models.CharField(max_length=128, help_text="Street Address")
    city = models.CharField(max_length=64)
    history = HistoricalRecords()


class Visit(models.Model):
    client = models.ForeignKey('Client')
    visited_at = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

