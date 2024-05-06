from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class recipeURLstest(TestCase):
    def test_recipes_index_url_is_correct(self):
        home_url = reverse('recipes:index')
        self.assertEqual(home_url, '/')
    
    def test_recipes_category_url_is_correct(self):
        category_url = reverse('recipes:category', kwargs={'category_id': 1,})
        self.assertEqual(category_url, '/recipes/category/1/')

    def test_recipes_recipe_url_is_correct(self):
        recipe_url = reverse('recipes:recipe_detail', kwargs={'pk':1})
        self.assertEqual(recipe_url, '/recipe/1/')

    def test_recipes_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')