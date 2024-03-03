from django.core.exceptions import ValidationError
from parameterized import parameterized

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
         
