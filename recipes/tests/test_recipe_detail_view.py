from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase

from recipes import views


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        recipe_view = resolve(reverse('recipes:recipe_detail', kwargs={'recipe_id':1}))
        self.assertEqual(recipe_view.func, views.recipe_detail)

    def test_recipe_detail_view_loads_correct_template(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'recipe_id':1}))
        self.assertTemplateUsed(response, 'recipes/html/recipe_detail.html')

    def test_recipe_detail_view_returns_status_code_200_ok(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'recipe_id':1}))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_returns_404_if_no_recipes_found_ok(self):
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'recipe_id':10000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_loads_recipes(self):
        needed_title = 'This is a Recipe_detail test - it load one recipe'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'recipe_id':1}))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipe_detail_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 404)
