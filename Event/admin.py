from django.contrib import admin
from .models import Contact,Event,Timetable
# Register your models here.
admin.site.register(Contact)
admin.site.register(Event)
admin.site.register(Timetable)