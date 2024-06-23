import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest

@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_sucessfully(self):
        user_password = 'pass'
        user = User.objects.create_user(username='user_test', password=user_password)
        
        # User open the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        #user looks to the form
        form = self.browser.find_element(By.CLASS_NAME, 'login-form')
        username_field = self.get_element_by_placeholder(form, 'Type your username here')
        password_field = self.get_element_by_placeholder(form, 'Type your password here')
        
        # User type his username and password
        username_field.send_keys(user.username)
        password_field.send_keys(user_password)
        
        #User send the form
        form.submit()
        
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        
        self.assertIn(f'You are logged in as: {user.username}.' , body)
        
        
    def test_form_login_is_invalid(self):
        #User open login page
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        #user see the login form
        form = self.browser.find_element(By.CLASS_NAME, 'login-form')
        
        #and tryto send empty values
        username = self.get_element_by_placeholder(form, 'Type your username here')
        password = self.get_element_by_placeholder(form, 'Type your password here')
        username.send_keys(' ')
        password.send_keys(' ')
        
        #user send the form
        form.submit()
        
        #user see the error message
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Invalid username or password.', body)
    
    
    def test_form_login_invalid_credentials(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        
        form = self.browser.find_element(By.CLASS_NAME, 'login-form')
        username = self.get_element_by_placeholder(form, 'Type your username here')
        password = self.get_element_by_placeholder(form, 'Type your password here')
        
        username.send_keys('User_test')
        password.send_keys('Strongpass123')
        
        form.submit()
        
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Invalid credentials.', body)
        
        
        