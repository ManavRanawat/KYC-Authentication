from django.db import models

# Create your models here.

class Passport(models.Model):
    passport_no = models.CharField(max_length=50)
    date_of_issue = models.DateField()
    date_of_expiry = models.DateField()
    name=models.CharField(max_length=100)

class Driving_License(models.Model):
    dl_no = models.CharField(max_length=50)
    date_of_issue = models.DateField()
    date_of_expiry = models.DateField()
    name=models.CharField(max_length=100)

class PanCard(models.Model):
    pancard_no = models.CharField(max_length=50)
    name=models.CharField(max_length=100)
