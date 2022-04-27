from django.core.mail import send_mail
from celery import shared_task
import time
from Event import telegrambot
from django.contrib.auth.models import User
# celery -A Event worker -l info -P gevent


@shared_task
def send_reminder_mail(num,reciver_email,reciver_name,reciver_event,reciver_id): 
    id = telegrambot.get_id(reciver_name)
    if id != reciver_id :
        User.objects.filter(username = reciver_name).update(id = id)
        telegrambot.send_message(f"Dear {reciver_name},Your telegram id is recorded,you will recive messages of Your reminder here.\nTeam Timetable",id)
        telegrambot.send_message(f"Dear {reciver_name},we would like to remind you your reminder of {reciver_event}.\nThank You.\nTeam Timetable",id)
        return None
    time.sleep(num)
    send_mail(
        "Event-Reminder",
        f"Dear {reciver_name},we would like to remind you your reminder of {reciver_event}. \nThank You \nTeam Timetable",
        "jha.dhiraj22803@gmail.com",
        [f"{reciver_email}"],
        fail_silently = False
    
    )
    telegrambot.send_message(f"Dear {reciver_name},we like to remind you your reminder of {reciver_event}. \nThank You \nTeam Timetable",
    reciver_id)
    return None


    
