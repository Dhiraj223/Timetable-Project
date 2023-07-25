from django.db import models
from django.db.models.base import Model

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    tele = models.CharField(max_length=13)
    content = models.TextField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return "Contact by - " + self.name

class Event(models.Model):
    username = models.CharField(max_length=200)
    types = models.CharField(max_length=200)
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    event = models.TextField(max_length=200000)
    

    def __str__(self):
        return "Remainder of - " + self.username + " "+ self.event

class Timetable(models.Model):
    username = models.CharField(max_length=200)
    time = models.TextField(blank=True)
    topic = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Remainder of - " + self.username
    
class TeleId(models.Model):
    username = models.CharField(max_length=200)
    teleid   = models.CharField(max_length=100, default="0000000")
    num_mes  = models.CharField(max_length=200, default=1)

    def __str__(self):
        return "Users Telegram Ids - " + self.username