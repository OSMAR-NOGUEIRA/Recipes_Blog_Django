from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
import pytest
import time

from .base import AuthorsBaseTest

@pytest.mark.functional_test
class TestAuthorEditProfileView(AuthorsBaseTest):
    def test_authors_edit_profile_view_updates_itself_when_form_is_valid_and_submited(self):
        user = self.create_and_login_user()
        edit_profile_url = reverse('authors:profile_edit', kwargs={'pk':user.profile.id})
        
        self.browser.get(self.live_server_url + edit_profile_url)
        
        form = self.browser.find_element(By.CLASS_NAME, 'profile-edit-form')
        
        profile_bio_field = self.browser.find_element(By.ID, 'id_bio')
        profile_bio_field.send_keys('Testing profile bio.')
        form.submit()
        
        profile_view_url = reverse('authors:profile', kwargs={'id': user.profile.id})
        self.browser.get(self.live_server_url + profile_view_url)
        
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        
        self.assertIn('Testing profile bio.', body)