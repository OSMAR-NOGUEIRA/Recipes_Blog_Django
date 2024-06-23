from django.core.exceptions import ValidationError
from parameterized import parameterized
from unittest.mock import patch
from PIL import Image
from django.conf import settings
import os

from recipes.models import Recipe
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipes_no_default(self):
         recipe = Recipe(
            title = 'Recipe Title',
            description = 'Recipe Description',
            slug = 'Recipe-Slug-no-default',
            preparation_time = 20,
            preparation_time_unit = 'Minutes',
            servings = 4,
            servings_unit = 'Portions',
            preparation_steps ='Recipe Preparation steps',
            #preparation_steps_is_html = False,         # we dont set thoes fields because they gonna get theirs default value in the model Recipe
            #is_published = True,                       # we dont set thoes fields because they gonna get theirs default value in the model Recipe
            category = self.make_category(name='Test Default Category'),
            author = self.make_author(username='newuser'),
                    )
         recipe.full_clean()
         recipe.save()
         return recipe
    
    def test_recipe_title_raises_error_if_title_has_more_then_65_chars(self):
        self.recipe.title = 'A' * 70 # creating a title with more than 65 chars
        with self.assertRaises(ValidationError): # assertRaises verify if some erros was raised
            self.recipe.full_clean() # recipe.full_clean() makes the validation in the model recipe and its gonna find the error in recipe.title

    @parameterized.expand([
            #('title', 65),#the title field test already has been made
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_lenght(self, field, max_length):
            setattr(self.recipe, field, 'A' * (max_length + 1))# setattr RECEBE UM OBJETO, O NOME DO CAMPO E UMA STRING QUE ENTRARA NO OBJETO E PASSARA O VALOR DA STRING PARA O ATRIBUTO DO OBJETO.
            with self.assertRaises(ValidationError): # assertRaises verify if some erros was raised
                self.recipe.full_clean() # recipe.full_clean() makes the validation in the model recipe and its gonna find the error in recipe.title

    def test_recipe_prepation_steps_is_html_is_false_by_default(self):
         recipe = self.make_recipes_no_default()
         self.assertFalse(recipe.preparation_steps_is_html, 
                          msg='Recipe preparation_steps_is_html can not be True by default')
         
    def test_recipe_is_published_is_false_by_default(self):
         recipe = self.make_recipes_no_default()
         self.assertFalse(recipe.is_published, 
                          msg='Recipe is_published can not be True by default')

    def test_class_recipe_str_representation(self):
         needed = 'Testing Representation'
         self.recipe.title = 'Testing Representation'
         self.recipe.full_clean()
         self.recipe.save()
         self.assertEqual(str(self.recipe), needed,
                        msg=f'Recipe string representation must be '
                            f'"{needed}" but "{str(self.recipe)}" was received!')
         
    def test_recipe_manager_returns_only_published_recipes(self):
        recipe_not_published = self.make_recipe(is_published=False, title='Recipe not published')
        recipe_published = self.make_recipe(is_published=True, title='Recipe published')
        
        recipes = Recipe.objects.get_published_recipes()
        
        self.assertNotIn(recipe_not_published, recipes)
        self.assertIn(recipe_published, recipes)
   
   
    def test_recipe_model_resize_image_ok(self):
        recipe = self.make_recipe(
            cover='/Users/osmarnogueira/Documents/Code_base/Django_Udemy/Section11/Django-project1/recipes/tests/assets/img.jpg'
            )
        img = recipe.cover
        image_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        original_image_pillow = Image.open(image_full_path)
        original_width, original_height = original_image_pillow.size
        
        img_new_width = 100
        
        Recipe.resize_image(image=img, new_width=img_new_width)
        
        image_pillow = Image.open(image_full_path)
        
        new_width, new_height = image_pillow.size
        
        self.assertEqual(new_height, (int((new_width * original_height) / original_width)))
        self.assertEqual(new_width, img_new_width)
        
        Recipe.resize_image(image=img, new_width=original_width, force=True)
        
        
    def test_recipe_model_slug_is_been_generate_if_no_slug_passed_ok(self):
        recipe = self.make_recipe(title='title recipe test', slug=None)
        intended_slug = 'Title-recipe-test'
        self.assertEqual(recipe.slug, intended_slug)
        
    def test_recipe_model_method_resize_image_does_not_break_aplication(self):
        false_cover_path = '/nonefile'
        recipe = self.make_recipe(cover=false_cover_path)
        self.assertEqual(recipe.cover.url, f'/media{false_cover_path}')