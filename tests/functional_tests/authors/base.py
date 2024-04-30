from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
import time

from utils.browser import make_chrome_browser

class AuthorsBaseTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser('--headless')
        
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self, qtd=10):
        time.sleep(qtd)
        
    def get_element_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')
        