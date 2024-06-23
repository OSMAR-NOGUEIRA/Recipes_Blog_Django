from django.urls import reverse
from recipes.tests.test_recipe_base import RecipeTestBase
from django.contrib.auth.models import User
from unittest import TestCase

from authors.forms import recipe_edit_form


class AuthorEditRecipeFormTest(TestCase):
    def test_func__is_positive_number_ok(self):
        value='-20'
        test_1 = recipe_edit_form.is_positive_number(value)
        self.assertEqual(test_1, False)
        
        value2='20'
        test_2 = recipe_edit_form.is_positive_number(value2)
        self.assertEqual(test_2, True)
        
        value3='A'
        test_3 = recipe_edit_form.is_positive_number(value3)
        self.assertEqual(test_3, False)

class AuthorEditRecipeFormFieldsTest(RecipeTestBase):
    def setUp(self) -> None:
        self.form_data = {
            'title':'Test',
            'description':'Description test',
            'preparation_steps': 'Testing',
            'preparation_time':'20',
            'preparation_time_unit':'Minutes',
            'servings':'5',
            'servings_unit':'people',
        }
        return super().setUp()
    
    def test_preparation_time_is_positive_number(self):
        user = User.objects.create_user(username='User_test', password='my_pass')
        self.client.login(username='User_test', password='my_pass')
        
        recipe = self.make_recipe(author_data=user, is_published=False)
        recipe_id = recipe.id
        
        self.form_data['preparation_time'] = '-20'
        url = reverse('authors:recipe_edit', kwargs={'recipe_id':recipe_id})
        
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertIn('Preparation time must be a positive number.', response.content.decode('utf-8'))
        
        
    def test_title_is_diferent_than_description_and_have_at_least_4_chars(self):
        user = self.make_author(username='User_test', password='my_pass')
        self.client.login(username=user.username, password='my_pass')
        
        recipe = self.make_recipe(author_data=user, is_published=False)
        recipe_id = recipe.id
        
        self.form_data['title'] = 'Tes'
        url = reverse('authors:recipe_edit', kwargs={'recipe_id':recipe_id})
        
        response1 = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn('Title must have at least 3 characters.', response1.content.decode('utf-8'))
        
        self.form_data['description'] = 'Tes'
        
        response2 = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn('Title can not be same as description.', response2.content.decode('utf-8'))
       
       
    def test_servings_is_a_positive_number(self):
        user = self.make_author(username='User_test', password='My_pass123')
        self.client.login(username=user.username, password='My_pass123')
        recipe = self.make_recipe(author_data=user, is_published=False)
        
        url = reverse('authors:recipe_edit', kwargs={'recipe_id':recipe.id})
        self.form_data['servings'] = '-5'
        
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn('Servings must be a positive number.', response.content.decode('utf-8'))