import os

from FIleUtil import create_empty_file, get_lines
from LogPrint import print_green, print_uncolored, print_red, print_blue_line, print_title
from User import User


class Setup:

    def __init__(self):
        self.last_message_admin_file_path = ""
        self.users_list = []
        self.active_users_list_file_path = ""

    def init(self):

        print_blue_line()

        print_title("\n\tADMIN SETUP\n")
        try:
            self.last_message_admin_file_path = self.__admin_setup()
        except Exception as e:
            print_red("ERROR",
                      f"The following exception was thrown during the Admin setup: {type(e).__name__}")
            raise Exception
        print_green("INFO", "Successfully Admin setup")
        print()

        print_blue_line()

        print_title("\n\tUSER INFO FOLDER SETUP\n")
        try:
            self.__users_info_folder_setup()
        except Exception as e:
            print_red("ERROR",
                      f"The following exception was thrown during the Users info folder setup: {type(e).__name__}")
            raise Exception
        print_green("INFO", "Successfully Users info folder setup")
        print()

        print_blue_line()

        print_title("\n\tPOPULATING USER LIST FROM FILE\n")
        try:
            users_list_info = self.__populate_users_list_from_users_file()
            for user_info in users_list_info:
                print()
                user = User(user_name=user_info[0],
                            bot_token=user_info[1],
                            chat_id=user_info[2])
                self.users_list.append(user)
        except Exception as e:
            print_red("ERROR",
                      f"The following exception was thrown during the users list population: {type(e).__name__}")
            raise Exception
        print()
        print_uncolored("INFO",
                        f"users_list = ")
        self.__print_list(users_list_info)
        print_green("INFO", "Successfully populated users list")
        print()

        print_blue_line()

        print_title("\n\tSTARTING THE ROUTIN\n")

        self.active_users_list_file_path = f".{os.sep}Users Info{os.sep}users_list.txt"

    def __admin_setup(self):
        admin_folder_path = f".{os.sep}Admin"
        last_message_admin_file_path = f".{os.sep}Admin{os.sep}last_message.txt"
        try:
            print_uncolored("INFO",
                            "Creating Admin folder")
            os.makedirs(admin_folder_path)
            print_uncolored("INFO",
                            "Creating last message file")
            create_empty_file(last_message_admin_file_path)
        except FileExistsError:
            print_uncolored("INFO",
                            "Admin folder and last message file already exist")

        return last_message_admin_file_path

    def __users_info_folder_setup(self):
        users_info_folder_path = f".{os.sep}Users Info"
        active_users_list_file_path = f"{users_info_folder_path}{os.sep}users_list.txt"
        try:
            print_uncolored("INFO",
                            "Creating Users Info folder")
            os.makedirs(users_info_folder_path)
            print_uncolored("INFO",
                            "Creating users list file")
            create_empty_file(active_users_list_file_path)
        except FileExistsError:
            print_uncolored("INFO",
                            "Users Info folder and Users list file already exist")

    def __populate_users_list_from_users_file(self):
        active_users_list_file_path = f".{os.sep}Users Info{os.sep}users_list.txt"
        users = get_lines(active_users_list_file_path)
        print_uncolored("\nINFO",
                        f"Found {len(users)} active users\n")
        users_list = []
        for user in users:
            info = user.split("--", 2)
            users_list.append([info[0].strip(), info[1].strip(), info[2].strip()])
        return users_list

    def __print_list(self, users_list):
        for user in users_list:
            print(user)
