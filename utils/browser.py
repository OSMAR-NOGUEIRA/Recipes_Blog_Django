from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from pathlib import Path
from time import sleep
import os


ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver'

CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME


def make_chrome_browser(*options):
    chrome_option = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_option.add_argument(option)

    chrome_services = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_services, options=chrome_option)
    return browser

if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('https://www.udemy.com/')
    sleep(5)
    browser.quit()
