from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
        
class Event(models.Model):
    event_name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    organizing_club = models.CharField(max_length=100)
    event_description = models.TextField()

    def __str__(self):
        return self.event_name

class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    branch = models.CharField(max_length=100)
    semester = models.IntegerField()
    clubs = models.ManyToManyField(Club)
    email = models.EmailField()


    def __str__(self):
        return self.full_name

class Notification(models.Model):
    headline = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.headline
