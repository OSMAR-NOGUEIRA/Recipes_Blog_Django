from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class Recipe_views_tests(RecipeTestBase):

    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, views.RecipeListViewSearch)

    def test_recipe_search_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/html/search.html')
    
    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<test>'
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertIn('&lt;test&gt; | Recipes', content)