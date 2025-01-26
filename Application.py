from colorama import init

import os
from TelegramManager.MessageManager import MessageManager
from Routine import Routine
from Setup import Setup
from dotenv import load_dotenv

def main():

    load_dotenv()

    BOT_TOKEN_ADMIN = os.getenv("BOT_TOKEN_ADMIN")
    CHAT_ID_ADMIN = os.getenv("CHAT_ID_ADMIN")

    init()

    setup = Setup()
    setup.init()

    print()

    routine = Routine(users_list=setup.users_list,
                      active_users_list_file_path=setup.active_users_list_file_path,
                      admin_message_manager=MessageManager(bot_token=BOT_TOKEN_ADMIN,
                                                           chat_id=CHAT_ID_ADMIN,
                                                           last_message_file_path=setup.last_message_admin_file_path))
    routine.start()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        pass
