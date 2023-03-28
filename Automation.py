from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium import webdriver
import time
import urllib
import os
from urllib.parse import urlparse, unquote


class Automation:
    def __init__(self, driver: webdriver):
        self.driver = driver
        self.wait120 = WebDriverWait(self.driver, 120)
        self.reports_dictionary = {
            "Cost overview": "2", "Usage overview": "5", "Enhanced User profile report": "10"}

    def login(self, user):
        self.driver.get("https://entreprise.bell.ca/corporateselfserve/login")
        email = self.driver.find_element(
            By.XPATH, "//input[@id='usernameField']")
        email.send_keys(user.email)

        password = self.driver.find_element(
            By.XPATH, "//input[@id='passwordField']")
        password.send_keys(user.password)

        login_button = self.driver.find_element(
            By.XPATH, "//button[@id='submitBtn']")
        login_button.click()

    def look_for_reports(self):
        # html is using a javascript framework, so we have to wait for javascript requests to finish, for that we will use time.sleep
        time.sleep(60)
        reports_tab = self.wait120.until(EC.presence_of_element_located(
            (By.XPATH, "//header/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/nav[1]/ul[1]/li[4]")))
        actions = ActionChains(self.driver)
        actions.move_to_element(reports_tab).perform()

        e_reporting = self.driver.find_element(
            By.XPATH, "//header/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/nav[1]/ul[1]/li[4]/div[1]/ul[1]/li[1]/a[1]")
        e_reporting.click()

        time.sleep(60)

        # get tabs open
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])  # switch to second tab
        standard_reports = self.driver.find_element(
            By.XPATH, "//a[contains(text(),'Standard reports')]")
        standard_reports.click()
        time.sleep(20)

    def select_and_download(self):
        # select other options
        select = Select(self.driver.find_element(
            By.XPATH, "//select[@id='reportsDropDown']"))

        records = 0
        for key, value in self.reports_dictionary.items():
            print(f"getting: {key}")
            try:
                select.select_by_value(value)
                time.sleep(5)
                excel_image = self.driver.find_element(
                    By.XPATH, "//body/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/img[2]")
                excel_image.click()
                records = records + 1
            except Exception:
                print(f"something happened with {key}")

        time.sleep(60*8)
        directory_path = os.getcwd()
        status_board = self.driver.find_element(
            By.XPATH, "//body/div[@id='reportStatusBar']/div[@id='reportStatusBarContent']/div[@id='reportStatusBarRequests']/table[1]")
        rows = status_board.find_elements(By.TAG_NAME, "tr")
        rows = rows[:records]  # first three rows are three first reports
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            download_link = cells[0].find_element(By.TAG_NAME, 'a')
            download_link.click()
            url_file = download_link.get_attribute('href')
            parsed_url = urlparse(url_file)
            filename = parsed_url.query.split('=')[2]
            filename = unquote(filename).replace('+', ' ')
            print(f"downloaded filename: {filename}")

        time.sleep(60*2)  # time to wait for download.
