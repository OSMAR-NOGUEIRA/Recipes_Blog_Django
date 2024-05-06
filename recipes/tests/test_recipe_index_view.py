from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
import math
from unittest.mock import patch

from recipes import views
from utils.generateFakes import make_batch_of_recipes



class RecipeIndexViewTest(RecipeTestBase):
    def test_recipes_index_view_function_is_correct(self):
        index_view = resolve(reverse('recipes:index'))
        self.assertIs(index_view.func.view_class, views.RecipeListViewHome)

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
        ...
        response_context = response.context['recipes'].object_list[0]
        self.assertEqual(response_context.id, 1)
        self.assertEqual(response_context.title, 'Receita nova')

    def test_recipe_index_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:index'))
        content = response.content.decode('utf-8')
        self.assertIn('<h1>You have no recipes to be shown yet.</h1>', content)

    @patch('recipes.views.PER_PAGE', new=9)# patch modifica o valor da variavel somente para uso no test e depois volta o valor oirginal da mesma
    def test_recipe_index_pagination_loads_9_itens_per_page_ok(self):
        #for i in range(36):
        #    kw = {'slug': f'r{i}', 'author_data':{'username': f'u{i}'}}        # to slow 
        #    self.make_recipe(**kw)

        number_of_objects = 18
        recipes = make_batch_of_recipes(number_of_objects)

        response = self.client.get(reverse('recipes:index'))
        
        self.assertEqual(len(response.context['recipes'].object_list), 9)

    @patch('recipes.views.PER_PAGE', new=9)# patch modifica o valor da variavel somente para uso no test e depois volta o valor oirginal da mesma
    def test_recipes_index_pagination_loads_correct_number_of_pages(self):
        number_of_objects = 45
        recipes = make_batch_of_recipes(number_of_objects)

        response = self.client.get(reverse('recipes:index'))
        qty_pgs = response.context['recipes'].paginator.num_pages

        self.assertEqual(qty_pgs, math.ceil(number_of_objects/9) )

    @patch('recipes.views.PER_PAGE', new=9)# patch modifica o valor da variavel somente para uso no test e depois volta o valor oirginal da mesma
    def test_recipes_index_pagination_loads_correct_page(self):
        recipes = make_batch_of_recipes(50)
        page_needed = 3

        response = self.client.get(reverse('recipes:index') + f'?page={page_needed}')
        current_page = response.context['recipes'].number

        self.assertEqual(current_page, page_needed)
