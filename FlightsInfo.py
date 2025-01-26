from FIleUtil import get_lines, update_file_value, add_line, get_line
from Flight import Flight
from LogPrint import print_red, print_green
from WebUtil import create_driver
import random

RANDOM_NUMBERS_FILE_PATH = "random_numbers.txt"


class FlightsInfo:

    def __init__(self, fly_link_list_file_path, user_name, last_price_file_path_root):
        self.last_price_file_path_root = last_price_file_path_root
        self.user_name = user_name
        self.fly_link_list_file_path = fly_link_list_file_path
        self.flights_info_list = []
        self.get_flights_info()

    def get_flights_info(self):
        fly_links = get_lines(self.fly_link_list_file_path)
        i = 1
        tot_fly_links = len(fly_links)
        for fly_link in fly_links:
            try:
                company, random_number, link = self.parse_flylink(fly_link)
            except Exception as e:
                print_red(
                    "ERROR",
                    f"user={self.user_name}, The following exception was thrown parsing flylink = {fly_link} in get_flights_info(): {type(e).__name__}")
                raise Exception
            try:
                driver = create_driver(link=link,
                                       user_name=self.user_name)
            except Exception as e:
                print_red(
                    "ERROR",
                    f"user={self.user_name} company={company} link={link} \n\t"
                    f"The following exception was thrown during creation of the driver in get_flights_info(): {type(e).__name__}")
                raise Exception
            flight = Flight(company=company,
                            driver=driver,
                            link=link,
                            random_number=random_number)
            self.add_flights_info(flight)
            print_green("INFO",
                        f"User = {self.user_name}\n\tCorrectly setted link n. {i}/{tot_fly_links}")
            i += 1

    def add_fly_link(self, company, link):
        try:
            driver = create_driver(link=link,
                                   user_name=self.user_name)
        except Exception as e:
            print_red(
                "ERROR",
                f"user={self.user_name} company={company} link={link} \n\t"
                f"The following exception was thrown during creation of the driver in add_fly_link: {type(e).__name__}")
            raise Exception
        random_number = self.get_random_number()
        last_price_file_path = self.last_price_file_path_root + str(random_number) + "_.txt"
        update_file_value(file=last_price_file_path,
                          new_value="0")
        flight = Flight(company=company,
                        driver=driver,
                        link=link,
                        random_number=random_number)
        self.add_flights_info(flight)
        add_line(file=self.fly_link_list_file_path,
                 value=f"{company} -- {random_number} -- {link}")
        print_green("INFO",
                    f"User = {self.user_name}\n\tCorrectly added link={link}")

    def add_flights_info(self, flight):
        self.flights_info_list.append(flight)

    def parse_flylink(self, fly_link):
        parti = fly_link.split("--", 2)
        return parti[0].strip(), parti[1].strip(), parti[2].strip()

    def get_random_number(self):
        while True:
            random_number = str(random.randint(1, 1000))
            if random_number not in get_line(file=RANDOM_NUMBERS_FILE_PATH,
                                             string=True):
                break
        add_line(file=RANDOM_NUMBERS_FILE_PATH,
                 value=random_number)
        return random_number
