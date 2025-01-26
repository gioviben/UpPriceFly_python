import urllib.parse
import urllib.request
import json
import time

from LogPrint import print_green, print_red


class SendMessage:

    def __init__(self, bot_token, chat_id, last_message_file_path):
        self.query = None
        self.BOT_TOKEN = bot_token
        self.CHAT_ID = chat_id
        self.last_message_file_path = last_message_file_path
        self.message = ""

    def set_message(self, message):
        self.message = message
        self.query = {
            "chat_id": self.CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }

    def send_message(self):
        url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode(self.query).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")

        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")
            response_json = json.loads(response_data)

            if response_json["ok"]:
                print_green("INFO",
                            "Message sent correctly")
            else:
                print_red("ERROR",
                          f"Error sending the message\n\t--> {response_json['description']}")

        time.sleep(0.5)
