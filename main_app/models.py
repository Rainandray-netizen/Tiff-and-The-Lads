from django.db import models
from django.contrib.auth.models import User
import datetime

VENUE = (
    ('A', 'Outdoor'),
    ('B', 'Indoor')
)

TIME = (
    ('A', 'Less than 30 minutes'),
    ('B', 'Less than 2 hours'),
    ('C', 'More than 2 hours')
)

INTERACTION = (
    ('A', 'Low interaction'),
    ('B', 'Moderate interaction'),
    ('C', 'High interaction')
)

BOOL_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)

class Profile(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    profile_url = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=50)
    number_of_people = models.IntegerField()
    distancing = models.BooleanField(
        choices=BOOL_CHOICES
        )
    venue = models.CharField(
        max_length=1,
        choices=VENUE
    )
    time_length = models.CharField(
        max_length=1,
        choices=TIME
    )
    interaction = models.CharField (
        max_length=1,
        choices=INTERACTION
    ) 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    risk_level = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.name

class Routine(models.Model):
    date = models.DateField(default=datetime.date.today)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity = models.ManyToManyField(Activity)
    activity_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.activity)
    class Meta:
        ordering = ['date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for profile: {self.profile_id} @{self.url}"