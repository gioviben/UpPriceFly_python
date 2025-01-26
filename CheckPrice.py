from FIleUtil import get_line, update_file_value
from WebUtil import retrieve_field_value
from datetime import datetime
from TelegramManager.MessageManager import MessageManager
from LogPrint import print_uncolored, print_red

RYANAIR_PRICE_XPATH = '/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/flights-summary/div/div[1]/journey-container/journey/div/div[2]/div/carousel-container/carousel/div/ul/li[3]/carousel-item/button/div[2]/flights-price/ry-price/span[{}]'


class CheckPrice:

    def __init__(self, user_name):
        self.user_name = user_name

    def check_price(self, company, link, driver, message_manager, last_price_file_path):

        actual_price = self.retrieve_price(driver=driver, company=company)

        self.check_lowest_price(company=company,
                                link=link,
                                messagge_manager=message_manager,
                                actual_price=actual_price,
                                last_price_file_path=last_price_file_path)

    def retrieve_price(self, driver, company):
        driver.refresh()
        price = ''
        match company:
            case "RYANAIR":
                for index in range(2, 5):
                    value = retrieve_field_value(driver=driver,
                                                 xpath=RYANAIR_PRICE_XPATH.format(index))
                    price += value
                price = price.replace(',', '.')
                price = float(price)
        return price

    def check_lowest_price(self, company, link, messagge_manager: MessageManager, actual_price, last_price_file_path):
        try:
            last_price = get_line(last_price_file_path)
        except IOError as e:
            print_red("ERROR",
                      f"user={self.user_name} company={company} link={link} \n\tThe following IO error was thrown during the read process from {last_price_file_path} file: {type(e).__name__}")
            raise Exception
        except Exception as e:
            print_red(
                "ERROR",
                f"user={self.user_name} company={company} link={link} \n\tThe following exception was thrown during the read process from {last_price_file_path} file: {type(e).__name__}")
            raise Exception

        if actual_price < last_price:
            delta = round(last_price - actual_price, 2)
            print_uncolored("INFO",
                            f"user={self.user_name} company={company} link={link} \n\tIl prezzo si è abbassato di {delta}€ dall'ultima rilevazione")

            try:
                now = datetime.now()
                formatted_now = now.strftime("%d-%m-%Y %H:%M")

                messagge_manager.send_message.set_message(f"Ultima verifica: {formatted_now}\n"
                                                          f"Company = {company}\n"
                                                          f'<a href="{link}">Flight Link</a>\n'
                                                          f"Prezzo corrente {actual_price}€\n"
                                                          f"Il prezzo è sceso di -{delta}€ dall'ultima rilevazione ({last_price}€)")
            except Exception as e:
                print_red("ERROR",
                          f"user={self.user_name} company={company} link={link} \n\tThe following exception was thrown during the set_messagge process (case actual_price < last_price): {type(e).__name__}")
                raise Exception

            try:
                messagge_manager.send_message.send_message()
            except Exception as e:
                print_red("ERROR",
                          f"user={self.user_name} company={company} link={link} \n\tThe following exception was thrown during the send_messagge process (case actual_price < last_price): {type(e).__name__}")
                raise Exception

            try:
                actual_price_str = str(actual_price)
                update_file_value(last_price_file_path, actual_price_str)
            except IOError as e:
                print_red("ERROR",
                          f"user={self.user_name} company={company} link={link} \n\tThe following IO error was thrown during the write process to {last_price_file_path} file (case actual_price < last_price): {type(e).__name__}")
                raise Exception
            except Exception as e:
                print_red("ERROR",
                          f"user={self.user_name} company={company} link={link} \n\tThe following exception was thrown during the write process to {last_price_file_path} (case actual_price < last_price): {type(e).__name__}")
                raise Exception

        elif actual_price > last_price:
            delta = round(actual_price - last_price, 2)
            print_uncolored("INFO",
                            f"user={self.user_name} company={company} link={link} \n\tIl prezzo si è alzato di {delta}€ dall'ultima rilevazione")

            try:
                now = datetime.now()
                formatted_now = now.strftime("%d-%m-%Y %H:%M")

                messagge_manager.send_message.set_message(f"Ultima verifica: {formatted_now}\n"
                                                          f"Company = {company}\n"
                                                          f'<a href="{link}">Flight Link</a>\n'
                                                          f"Prezzo corrente {actual_price}€\n"
                                                          f"Il prezzo è aumentato di +{delta}€ dall'ultima rilevazione ({last_price}€)")
            except Exception as e:
                print_red("ERROR",
                          f"user={self.user_name} company={company} link={link} \n\tThe following exception was thrown during the set_messagge process (case actual_price > last_price): {type(e).__name__}")
                raise Exception

            try:
                messagge_manager.send_message.send_message()
            except Exception as e:
                print_red("ERROR",
                          f"user={self.user_name} company={company} link={link} \n\tThe following exception was thrown during the send_messagge process (case actual_price > last_price): {type(e).__name__}")
                raise Exception

            try:
                actual_price_str = str(actual_price)
                update_file_value(last_price_file_path, actual_price_str)
            except IOError as e:
                print_red("ERROR",
                          f"user={self.user_name} company={company} link={link} \n\tThe following IO error was thrown during the write process to {last_price_file_path} (case actual_price > last_price): {type(e).__name__}")
                raise Exception
            except Exception as e:
                print_red("ERROR",
                          f"user={self.user_name} company={company} link={link} \n\tThe following exception was thrown during the write process to {last_price_file_path} file (case actual_price > last_price): {type(e).__name__}")
                raise Exception
        else:
            print_uncolored("INFO",
                            f"user={self.user_name} company={company} link={link}\n\t"
                            f"The price has not changed\n\t"
                            f"actual_price={actual_price} == {last_price}=last_price  ")
