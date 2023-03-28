from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from Automation import Automation
from Classes.Models.User import User
import argparse


parser = argparse.ArgumentParser(description='Start scraper')
parser.add_argument('--email', help='bell email')
parser.add_argument('--password', help='bell password')

args = parser.parse_args()

def start_automation_driver() -> webdriver:
    chrome_options = Options()
    driver_service = Service(
        executable_path="./chromedriver_win32.zip/chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    driver.maximize_window()
    return driver


driver = start_automation_driver()
automation = Automation(driver)
user = User(args.email, args.password)


automation.login(user)
automation.look_for_reports()
automation.select_and_download()
