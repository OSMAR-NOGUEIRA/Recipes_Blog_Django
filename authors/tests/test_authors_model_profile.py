from django.test import TestCase
from django.contrib.auth.models import User


class TestAuthorProfileModel(TestCase):
    def test_model_profile__str__method_is_returning_username(self):
        user = User.objects.create_user(username='User_test', password='Mypass123')
        profile = user.profile
        
        self.assertEqual("User_test's profile", str(profile))
        