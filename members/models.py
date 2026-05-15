# Create your models here.
from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    plan = models.CharField(max_length=50)
    join_date = models.DateField()

    def __str__(self):
        return self.name
