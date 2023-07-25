import time
import threading
from Event.models import TeleId
import telepot

# Replace YOUR_BOT_TOKEN with your actual bot token
bot = telepot.Bot('6678210094:AAGU81ktJ8Z3thrmf5Id6y3mTB2_P9UASVM')



def send_reminder_mail(num, reciver_name, reciver_event, reciver_id, num_message):
    if reciver_id == "0000000" :
        print("I am Here")
        def handle_messages(msg):
            text_recived = msg["text"]
            chat_id = msg['chat']['id']
            print("Recived : ", chat_id)

            if text_recived == reciver_name :
                TeleId.objects.filter(username=reciver_name).update(teleid=chat_id)
                print("Updated")
                message_text = f"Dear {reciver_name}, Your telegram id is recorded, you will start reciving 'Your reminder here'.\nTeam Timetable"
                bot.sendMessage(chat_id, message_text)
            else :
                bot.sendMessage(chat_id,"Invalid Username,try again")
                bot.message_loop(handle_messages)
                time.sleep(300)

    else :
        time.sleep(num)
        message_text = f"""Subject: Gentle Reminder: Upcoming Event for {reciver_name}\n\nDear {reciver_name},\nWe sincerely hope this message finds you in good health and high spirits. We write to kindly remind you of the forthcoming event,"{reciver_event}", scheduled as per your timetable.\n\nTeam Timetable"""
        bot.sendMessage(reciver_id, message_text)
        return None


def schedule(num, reciver_name, reciver_event, reciver_id, num_message):
    threading.Thread(target=send_reminder_mail, args=(
        num, reciver_name, reciver_event, reciver_id, num_message)).start()
