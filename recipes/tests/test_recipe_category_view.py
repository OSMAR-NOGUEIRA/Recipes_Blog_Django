from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
import math
from unittest.mock import patch

from recipes import views
from utils.generateFakes import make_batch_of_recipes


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipes_category_view_function_is_correct(self):
        category_view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1,}))
        self.assertEqual(category_view.func.view_class, views.RecipeListViewCategory)

    def test_recipes_category_view_loads_correct_template(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}))
        self.assertTemplateUsed(response, 'recipes/html/index.html')

    def test_recipes_category_view_returns_status_code_200_ok(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}))
        self.assertEqual(response.status_code, 200)
    
    def test_recipes_category_view_returns_404_if_no_recipes_found_ok(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':10000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_loads_recipes(self):
        needed_title = 'This is a Category test - It load all recipes about the Category'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipe_category_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':recipe.category.id}))
        self.assertEqual(response.status_code, 404)


    @patch('recipes.views.PER_PAGE', new=9)# patch modifica o valor da variavel somente para uso no test e depois volta o valor oirginal da mesma
    def test_recipe_category_pagination_loads_9_itens_per_page_ok(self):
        number_of_objects = 36
        recipes = make_batch_of_recipes(36, category='CategoryTest')
        category_id = recipes[0].category_id

        response = self.client.get(reverse('recipes:category' ,kwargs={'category_id':category_id}))
        self.assertEqual(len(response.context['recipes'].object_list), 9)

    @patch('recipes.views.PER_PAGE', new=9)# patch modifica o valor da variavel somente para uso no test e depois volta o valor oirginal da mesma
    def test_recipes_category_pagination_loads_correct_number_of_pages(self):
        number_of_objects = 45
        recipes = make_batch_of_recipes(number_of_objects, category='CategoryTest')
        category_id = recipes[0].category_id

        response = self.client.get(reverse('recipes:category', kwargs={'category_id':category_id}))
        qty_pgs = response.context['recipes'].paginator.num_pages
        self.assertEqual(qty_pgs, math.ceil(number_of_objects/9) )

    @patch('recipes.views.PER_PAGE', new=9)# patch modifica o valor da variavel somente para uso no test e depois volta o valor oirginal da mesma
    def test_recipes_category_pagination_loads_correct_page(self):
        recipes = make_batch_of_recipes(50, category='CategoryTest')
        category_id = recipes[0].category_id
        page_needed = 3
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}) + f'?page={page_needed}')
        current_page = response.context['recipes'].number
        ...
        self.assertEqual(current_page, page_needed)