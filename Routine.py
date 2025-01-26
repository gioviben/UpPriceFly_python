import time
from FIleUtil import add_line, get_line
from LogPrint import print_green, print_red, print_blue_line, print_blue, print_title
from datetime import datetime
from User import User
import schedule


class Routine:

    def __init__(self, users_list, active_users_list_file_path, admin_message_manager):
        self.MAX_TRY_NUMBER = 1
        self.users_list = users_list
        self.active_users_list_file_path = active_users_list_file_path
        self.admin_message_manager = admin_message_manager

    def start(self):

        self.__routine()

        schedule.every(30).minutes.do(lambda: self.__routine())
        try_number = 0

        while True:
            try:
                if try_number < self.MAX_TRY_NUMBER:
                    schedule.run_pending()
                    time.sleep(1)
                else:
                    print("ERROR --> max try number reached, closing the process...")
                    try:
                        self.admin_message_manager.send_message.set_message("An error occurs during the process,\n"
                                                                            "please contact the admin")
                        self.admin_message_manager.send_message.send_message()
                    except Exception:
                        pass
                    break
            except Exception as e:
                print(f"Trying the routine again, try_number n.{try_number}")
                try_number += 1

    def __routine(self):
        now = datetime.now()
        formatted_now = now.strftime("%d-%m-%Y %H:%M:%S")
        print_blue("INFO",
                   f"Last Check: {formatted_now}")

        last_admin_message = self.admin_message_manager.get_message.retrieve_last_message()

        if last_admin_message:
            info = last_admin_message.split("\n", 2)
            add_line(file=self.active_users_list_file_path,
                     value=last_admin_message.replace("\n", "--"))
            self.users_list.append(User(user_name=info[0],
                                   bot_token=info[1],
                                   chat_id=info[2]))
            self.admin_message_manager.send_message.set_message("New user correctly added")
            self.admin_message_manager.send_message.send_message()
            print_green("INFO",
                        "New user found, added to users list file")

        for user in self.users_list:
            print_title(f"\n\t\tUSER = {user.user_name}\n")
            last_message = user.message_manager.get_message.retrieve_last_message()
            if last_message:
                if "www." in last_message:
                    try:
                        company, link = self.__parse_company(last_message)
                    except Exception as e:
                        print_red(
                            "ERROR",
                            f"user={user.user_name}, The following exception was thrown parsing company in routine(): {type(e).__name__}\n\t"
                            f"New message found = {last_message}")
                        raise Exception

                    if link not in get_line(file=user.fly_link_list_file_path,
                                            string=True):
                        user.flights_info.add_fly_link(company=company,
                                                       link=link)
                        user.message_manager.send_message.set_message("Flight correctly added\n"
                                                                      "Starting to monitor")
                        user.message_manager.send_message.send_message()
            user.check_lowest_price()
        print_blue_line()

    def __parse_company(self, last_message):
        parti = last_message.split("\n", 1)
        return parti[0].upper().strip(), parti[1].strip()
