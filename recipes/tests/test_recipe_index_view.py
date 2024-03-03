from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve

from recipes import views



class RecipeIndexViewTest(RecipeTestBase):
    def test_recipes_index_view_function_is_correct(self):
        index_view = resolve(reverse('recipes:index'))
        self.assertIs(index_view.func, views.index)

    def test_recipes_index_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:index'))
        self.assertTemplateUsed(response, 'recipes/html/index.html')

    def test_recipes_index_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:index'))
        self.assertEqual(response.status_code, 200)

    def test_recipes_index_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:index'))
        self.assertIn('<h1>You have no recipes to be shown yet.</h1>', response.content.decode('utf-8'))

    def test_recipe_index_loads_recipes(self):
        #need a recipe for testing
        self.make_recipe(author_data={
            'first_name':'john',
        },title='Receita nova',
        category_data={'name':'breakfast'}
        )
        response = self.client.get(reverse('recipes:index'))
#############################################################
        response_content = response.content.decode('utf-8')
        self.assertIn('Receita nova', response_content)
        self.assertIn('john', response_content)
        self.assertIn('breakfast', response_content)
#############################################################
        response_context = response.context['recipes'].first()
        self.assertEqual(response_context.id, 1)
        self.assertEqual(response_context.title, 'Receita nova')

    def test_recipe_index_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:index'))
        content = response.content.decode('utf-8')
        self.assertIn('<h1>You have no recipes to be shown yet.</h1>', content)
        
