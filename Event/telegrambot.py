import requests
import json
import configparser as cfg

from requests.api import get

class tele_bot():

    def __init__(self):
        # self.base = f"https://api.telegram.org/bot1955570917:AAEABULD-Ul6izfHmHNnXK9RlDJYO4aGOBo"
        self.base = f"https://api.telegram.org/bot5359237413:AAHAaUDnMLnt-haBip2rcEw1KOy1N4Hq8bE"

    def get_updates(self,offset=None):
        url =self.base +"/getUpdates?timeout=30"
        if offset :
            url = url + f"&offset={offset+1}"
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self,msg,chat_id):
        url = self.base +f"/sendMessage?chat_id={chat_id}&text={msg}"
        print(url)
        if msg is not None:
            requests.get(url)
bot = tele_bot()

def get_id(username):
    update_id = None
    while True:
        updates = bot.get_updates(offset=update_id)
        updates = updates["result"]
        if updates :
            for item in updates:
                update_id = item["update_id"]
                message = str(item["message"]["text"])
                if message == username :
                    from_ = item["message"]["from"]["id"]
                    return from_
            else:
                return 0000000  
        

def send_message(msg,id):
    bot.send_message(msg,id)

