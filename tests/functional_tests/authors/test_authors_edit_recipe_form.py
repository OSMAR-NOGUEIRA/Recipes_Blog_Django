from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
import pytest

from .base import AuthorsBaseTest
from recipes.tests.test_recipe_base import RecipeMixin

@pytest.mark.functional_test
class AuthorEditRecipeForm(AuthorsBaseTest, RecipeMixin):
    def test_user_is_typing_positive_number_in_preparation_time_ok(self):
        password = 'My_pass'
        user = self.create_and_login_user(user_password=password)
        self.make_recipe(author_data=user, is_published=False)
        
        url = reverse('authors:dashboard')
        self.browser.get(self.live_server_url + url)
        recipe = self.browser.find_element(By.LINK_TEXT, 'Recipe Title')
        recipe.click()
        
        form = self.browser.find_element(By.CLASS_NAME, 'edit-recipe-form')
        
        preparation_time_field = self.get_element_by_placeholder(form, 'E.g. 50')
        
        preparation_time_field.clear()
        preparation_time_field.send_keys('20')
        form.submit()
        
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Preparation time must be a positive number.', body)
        
        #####################################################################
        form = self.browser.find_element(By.CLASS_NAME, 'edit-recipe-form')
        
        preparation_time_field = self.get_element_by_placeholder(form, 'E.g. 50')
        
        preparation_time_field.clear()
        preparation_time_field.send_keys('-20')
        form.submit()
        
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Preparation time must be a positive number.', body)
