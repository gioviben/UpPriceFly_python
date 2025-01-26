import json
import requests
import time

from FIleUtil import get_line, update_file_value
from LogPrint import print_red, print_yellow, print_uncolored, print_cyan


class GetMessage:

    def __init__(self, bot_token, last_message_file_path):
        self.BOT_TOKEN = bot_token
        self.last_message_file_path = last_message_file_path
        self.URL = "https://api.telegram.org/bot{}/".format(self.BOT_TOKEN)

    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js

    def get_updates(self, offset=None):
        url = self.URL + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js

    def get_last_chat_id_and_text(self, updates):
        try:
            num_updates = len(updates["result"])
            last_update = num_updates - 1
            text = updates["result"][last_update]["message"]["text"]
            chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        except IndexError:
            print_yellow("WARNING",
                         f"The IndexError exception was thrown during getting last chat id and text\n\t"
                         f"Assuming that no recent message was found")
            return None, None
        except KeyError:
            print_yellow("WARNING",
                         f"The KeyError exception was thrown during getting last chat id and text\n\t"
                         f"Assuming that no recent message was found")
            return None, None
        except Exception as e:
            print_red("ERROR",
                      f"The following exception was thrown during getting last chat id and text: {type(e).__name__}")
            raise Exception
        return text, chat_id

    def retrieve_last_message(self):
        last_textchat = get_line(file=self.last_message_file_path,
                                 string=True)
        try:
            js = self.get_updates()
        except Exception as e:
            print_red("ERROR",
                      f"The following exception was thrown getting chat updates: {type(e).__name__}")
            raise Exception
        text, chat = self.get_last_chat_id_and_text(js)
        if text is not None and chat is not None:
            if f"{text} {chat}" != last_textchat:
                # send_message(text, chat)
                print_cyan("INFO",
                           "Found new message = ",
                           f"\n{text}\n",
                           "")
                update_file_value(file=self.last_message_file_path,
                                  new_value=f"{text} {chat}")
                time.sleep(0.5)
                return text
            time.sleep(0.5)
            print_uncolored("INFO",
                            "No recent message was found")
        return None
