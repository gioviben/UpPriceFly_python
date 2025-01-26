import os

from CheckPrice import CheckPrice
from FIleUtil import create_empty_file
from FlightsInfo import FlightsInfo
from LogPrint import print_red
from TelegramManager.MessageManager import MessageManager


class User:

    def __init__(self, user_name, bot_token, chat_id):
        directory_exist = False
        try:
            os.makedirs(f".{os.sep}{user_name}")
            os.makedirs(f".{os.sep}{user_name}{os.sep}Last_Prices_Folder")
        except FileExistsError:
            directory_exist = True
        self.user_name = user_name
        self.last_message_file_path = f".{os.sep}{user_name}{os.sep}last_message.txt"
        self.last_price_file_path_root = f".{os.sep}{user_name}{os.sep}Last_Prices_Folder{os.sep}last_price_"
        self.fly_link_list_file_path = f".{os.sep}{user_name}{os.sep}fly_link_list.txt"
        if not directory_exist:
            create_empty_file(self.last_message_file_path)
            create_empty_file(self.fly_link_list_file_path)
        self.message_manager = MessageManager(bot_token=bot_token,
                                              chat_id=chat_id,
                                              last_message_file_path=self.last_message_file_path)
        self.check_price = CheckPrice(user_name=user_name)
        self.flights_info = FlightsInfo(user_name=self.user_name,
                                        last_price_file_path_root=self.last_price_file_path_root,
                                        fly_link_list_file_path=self.fly_link_list_file_path)

    def check_lowest_price(self):
        for flight_info in self.flights_info.flights_info_list:
            company = flight_info.company
            driver = flight_info.driver
            link = flight_info.link
            random_number = flight_info.random_number
            last_price_file_path = self.last_price_file_path_root + str(random_number) + "_.txt"
            try:
                self.check_price.check_price(company=company,
                                             link=link,
                                             driver=driver,
                                             message_manager=self.message_manager,
                                             last_price_file_path=last_price_file_path)
            except Exception:
                print_red("ERROR",
                          f"User = {self.user_name}, an exception was thrown during the check_price process\n\t"
                          f"Company = {company}, Link = {link}, Random_number = {random_number}\n\t"
                          f"Continuing with the next flight if any")
