from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class Recipe_views_tests(RecipeTestBase):
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
        


    def test_recipes_category_view_function_is_correct(self):
        category_view = resolve(reverse('recipes:category', kwargs={'category_id': 1,}))
        self.assertEqual(category_view.func, views.category)

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