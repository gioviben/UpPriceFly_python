from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from LogPrint import print_red, print_yellow

RYANAIR_COOKIE_POPUP = '//*[@id="cookie-popup-with-overlay"]/div/div[3]/button[2]'


def click_button(driver, xpath=None, timeout=30):
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))
    element.click()


def retrieve_field_value(driver, xpath=None,
                         try_number=0, time_out=30):
    try:
        if try_number >= 5:
            print_red(
                "ERROR", f"Error in retrieve_field_value() --> Max number of tries reached")
            raise Exception
        value = WebDriverWait(driver, time_out).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
        value_text = value.text
    except TimeoutException:
        print_red(
            "ERROR",
            f"Error in retrieve_field_value() --> Timeout Exception cathed, trying again n. {try_number}")
        value_text = retrieve_field_value(driver=driver,
                                          xpath=xpath,
                                          try_number=try_number + 1)
    except NoSuchElementException:
        if xpath:
            print_red(
                "ERROR",
                f"Error in retrieve_field_value() --> The selector {xpath} can't be found")
        raise Exception
    except Exception as e:
        print_red(
            "ERROR",
            f"Error in retrieve_field_value() --> A more general exception was thrown: {type(e).__name__}")
        raise Exception

    return value_text


def create_driver(link, user_name):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    close_cookie(driver=driver,
                 user_name=user_name)
    return driver


def close_cookie(driver, user_name):
    try:
        click_button(driver=driver,
                     xpath=RYANAIR_COOKIE_POPUP,
                     timeout=4)
    except NoSuchElementException:
        print_yellow("WARNING",
                     f"User={user_name} No cookie banner was found, continuing as usual")
    except Exception as e:
        print_red("ERROR",
                  f"User={user_name} The following exception was thrown during the close cookie banner process: {type(e).__name__}")
        raise Exception
