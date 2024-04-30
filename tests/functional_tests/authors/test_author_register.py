from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from django.urls import reverse

from .base import AuthorsBaseTest

@pytest.mark.functional_test
class AuthorRegisterTest(AuthorsBaseTest):
    def get_form(self):
        return self.browser.find_element(By.XPATH, '/html/body/div/main/form')
    
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed(): #you can only send keys for displayed inputs not for hidden ones
                field.send_keys(' ' * 20)
    
    def test_empty_inputs_show_errors(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        
        form = self.get_form()
        form.find_element(By.NAME, 'email').send_keys('email@invalid')
        
        self.fill_form_dummy_data(form)
        
        first_name_field = self.get_element_by_placeholder(form, 'e.g. John')
        first_name_field.send_keys(' ')
        first_name_field.send_keys(Keys.ENTER)
        
        form = self.get_form()
        
        self.assertIn('First name is required.', form.text)         #first name
        
        self.assertIn('Last name is required.', form.text)          #Last name
        
        self.assertIn('This field can not be empty.', form.text)    #username
        
        self.assertIn('Enter a valid email address.', form.text)    #email
               
        self.assertIn('Password must not be empty.', form.text)     #password
       
        self.assertIn('Please repeat your password.', form.text)    #check password
        
    def test_error_passwords_do_not_match_ok(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        
        form = self.get_form()
        form.find_element(By.NAME, 'email').send_keys('email@invalid')
        
        self.fill_form_dummy_data(form)
        
        password_field = self.get_element_by_placeholder(form, 'Your password')
        password2_field = self.get_element_by_placeholder(form, 'Repeat your password here')
        password_field.send_keys('StrongPass1234')
        password2_field.send_keys('StrongPass12345')
        
        password_field.send_keys(Keys.ENTER)
        
        form = self.get_form()

        self.assertIn("Those passwords didn’t match. Try again.", form.text)
        
    def test_valid_user_data_register_sucessfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        
        form = self.get_form()
        
        form.find_element(By.NAME, 'first_name').send_keys('User')
        form.find_element(By.NAME, 'last_name').send_keys('01')
        form.find_element(By.NAME, 'username').send_keys('user01TEST')
        form.find_element(By.NAME, 'email').send_keys('test@email.com')
        form.find_element(By.NAME, 'password').send_keys('StrongPass1234')
        form.find_element(By.NAME, 'password2').send_keys('StrongPass1234')
        
        form.submit()
        
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        
        self.assertIn('User created sucessfully! Please log in.', body)
    
    def test_login_create_raises_404_if_request_not_post(self):
        request = self.browser.get(self.live_server_url + reverse('authors:login_create'))
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        
        self.assertIn('Not Found', body)
        

