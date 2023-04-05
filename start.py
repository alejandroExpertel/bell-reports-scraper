from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from Automation import Automation
from Classes.Models.User import User
from utils import get_driver_path, get_month_name_folder
import argparse
import os
import time


parser = argparse.ArgumentParser(description='Start scraper')
parser.add_argument('--email', help='bell email')
parser.add_argument('--password', help='bell password')
parser.add_argument('--server', help='macOS or windows')

args = parser.parse_args()


def start_automation_driver(user, server, date=None) -> webdriver:
    chrome_options = Options()
    prefs = {
        "download.default_directory": os.path.join(os.getcwd(), "Downloads", user.email.split('@')[0], get_month_name_folder(date)),
        "download.directory_upgrade": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver_service = Service(
        executable_path=get_driver_path(server))
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    driver.maximize_window()
    return driver


start_time = time.time()

user = User(args.email, args.password)
driver = start_automation_driver(user, args.server)
automation = Automation(driver)


automation.login(user)
automation.look_for_reports()
#automation.select_date_range('Jan 2023')
automation.select_and_download()
end_time = time.time()

print(f"It took: {end_time - start_time}")
