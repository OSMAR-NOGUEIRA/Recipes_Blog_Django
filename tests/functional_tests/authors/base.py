from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
import time
from django.urls import reverse

from utils.browser import make_chrome_browser

class AuthorsBaseTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser('--headless') #'--headless'
        
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self, qtd=10):
        time.sleep(qtd)
        
    def get_element_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')
        
        
    def create_and_login_user(self, user_username='User_test', user_password='My_pass123@'):
        from django.contrib.auth.models import User
        
        user = User.objects.create_user(username=user_username, password=user_password)
        
        url = reverse('authors:login')
        self.browser.get(self.live_server_url + url)
        
        form = self.browser.find_element(By.CLASS_NAME, 'login-form')
        
        username_field = self.get_element_by_placeholder(
            form,
            'Type your username here',
            )
        password_field = self.get_element_by_placeholder(
            form,
            'Type your password here',
            )
        
        username_field.send_keys(user.username)
        password_field.send_keys(user_password)
        
        form.submit()
        return user