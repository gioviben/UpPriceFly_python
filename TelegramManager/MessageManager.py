from TelegramManager.GetMessage import GetMessage
from TelegramManager.SendMessage import SendMessage


class MessageManager:

    def __init__(self, bot_token, chat_id, last_message_file_path):
        self.send_message = SendMessage(bot_token=bot_token,
                                        chat_id=chat_id,
                                        last_message_file_path=last_message_file_path)
        self.get_message = GetMessage(bot_token=bot_token,
                                      last_message_file_path=last_message_file_path)

    def set_message(self, text_message):
        self.send_message.set_message(text_message)

    def send_message(self):
        self.send_message.send_message()

    def get_last_message(self):
        return self.get_message.retrieve_last_message()
