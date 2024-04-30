from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
import math
from unittest.mock import patch #biblioteca para modificar o valor de uma variavel de dentro das views ou outro arquivo do app

from recipes import views
from utils.generateFakes import make_batch_of_recipes

class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertEqual(resolved.func, views.search)

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
    
    def test_recipe_search_can_find_recipe_by_title(self):
        title_1 = 'This is recipe one'
        title_2 = 'this is recipe two'
        recipe_1 = self.make_recipe(title=title_1, slug='title-1',author_data={'username':'one'})
        recipe_2 = self.make_recipe(title=title_2)
    
        response_1 = self.client.get(reverse('recipes:search')+ f'?q={title_1}')
        response_2 = self.client.get(reverse('recipes:search')+ f'?q={title_2}')
        response_both = self.client.get(reverse('recipes:search')+ f'?q=this')
     
        self.assertIn(recipe_1, response_1.context['recipes'])
        self.assertNotIn(recipe_2, response_1.context['recipes'])

        self.assertIn(recipe_2, response_2.context['recipes'])
        self.assertNotIn(recipe_1, response_2.context['recipes'])

        self.assertIn(recipe_1, response_both.context['recipes'])
        self.assertIn(recipe_2, response_both.context['recipes'])

    def test_recipe_search_can_find_recipe_by_description(self):
        description_1 = 'This is description one'
        description_2 = 'This is description two'

        recipe_1 = self.make_recipe(description=description_1,
                         author_data={'username':'one'},
                         slug='d-one')
        recipe_2 = self.make_recipe(description=description_2)

        response_1 = self.client.get(reverse('recipes:search')+ f'?q={description_1}')
        response_2 = self.client.get(reverse('recipes:search')+ f'?q={description_2}')
        response_both = self.client.get(reverse('recipes:search')+ f'?q=this')
     
        self.assertIn(recipe_1, response_1.context['recipes'])
        self.assertNotIn(recipe_2, response_1.context['recipes'])

        self.assertIn(recipe_2, response_2.context['recipes'])
        self.assertNotIn(recipe_1, response_2.context['recipes'])

        self.assertIn(recipe_1, response_both.context['recipes'])
        self.assertIn(recipe_2, response_both.context['recipes'])

    @patch('recipes.views.PER_PAGE', new=9) # patch modifica o valor da variavel somente para uso no test e depois volta o valor oirginal da mesma
    def test_recipe_search_pagination_loads_9_itens_per_page_ok(self):
        number_of_objects = 36
        recipes = make_batch_of_recipes(number_of_objects , title_for_all_recipes='Recipes_Search Pagination Test')
        response = self.client.get(reverse('recipes:search') + '?q=Recipes_Search Pagination Test')
        self.assertEqual(len(response.context['recipes'].object_list), 9)

    @patch('recipes.views.PER_PAGE', new=9)# patch modifica o valor da variavel somente para uso no test e depois volta o valor oirginal da mesma
    def test_recipes_search_pagination_loads_correct_number_of_pages(self):
        number_of_objects = 45
        recipes = make_batch_of_recipes(number_of_objects, title_for_all_recipes='Recipes_Search Pagination Test')
        response = self.client.get(reverse('recipes:search') + '?q=Recipes_Search Pagination Test')
        qty_pgs = response.context['recipes'].paginator.num_pages
        self.assertEqual(qty_pgs, math.ceil(number_of_objects/9) )

    @patch('recipes.views.PER_PAGE', new=9)# patch modifica o valor da variavel somente para uso no test e depois volta o valor oirginal da mesma
    def test_recipes_search_pagination_loads_correct_page(self):
        recipes = make_batch_of_recipes(50, title_for_all_recipes='Recipes_Search Pagination Test')
        page_needed = 3
        response = self.client.get(reverse('recipes:search') + f'?page={page_needed}' + '&q=Recipes_Search Pagination Test')
        current_page = response.context['recipes'].number
        self.assertEqual(current_page, page_needed)
