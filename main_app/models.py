from django.db import models
from django.contrib.auth.models import User

VENUE = (
    ('A', 'Outdoor'),
    ('B', 'Indoor')
)

TIME = (
    ('A', 'Less than 30 minutes'),
    ('B', 'Less than 2 hours'),
    ('C', 'More than 2 hours')
)

Interaction = (
    ('A', 'Low interaction'),
    ('B', 'Moderate interaction'),
    ('C', 'High interaction')
)

class Activity(models.Model):
    name = models.CharField(max_length=50)
    number_of_people = models.IntField()
    distancing = models.BooleanField
    venue = models.CharField(
        choices=Venue
    )
    time_length = models.CharField(
        choices=TIME
    )
    interaction = models.CharField (
        choices=INTERACTION
    ) 
    User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # def activity_assessment(self):


class Routine(models.Model):
    date = date.today("Date of Risk Assessment")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
