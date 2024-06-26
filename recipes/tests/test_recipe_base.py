from django.test import TestCase
from django.contrib.auth.models import User
from random import randrange

from recipes.models import Recipe, Category

class RecipeMixin():
    def make_category(self, name='category'):
        return Category.objects.create(name=name)
    
    def make_author(
            self, 
            username='user',
            first_name='name_1',
            last_name='name_2',
            password='12345678',
            email='a@email.com',
            ):
        
        username += f'user {randrange(1, 99)}'
        
        return User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
    
    def make_recipe(
            self,
            title = 'Recipe Title',
            description = 'Recipe Description',
            slug = 'Recipe-Slug',
            preparation_time = 20,
            preparation_time_unit = 'Minutes',
            servings = 4,
            servings_unit = 'Portions',
            preparation_steps ='Recipe Preparation steps',
            preparation_steps_is_html = False,
            is_published = True,
            category_data = None,
            author_data = None,
            cover = None,
                    ):

        if category_data is None:
            category_data = {}
        
        if author_data is None:
            author_data = {}
        
        return Recipe.objects.create(
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit,
            servings = servings,
            servings_unit = servings_unit,
            preparation_steps = preparation_steps,
            preparation_steps_is_html = preparation_steps_is_html,
            is_published = is_published,
            category = self.make_category(**category_data),
            author = author_data if type(author_data) is not dict else self.make_author(**author_data),
            cover = cover,
        )
        ...

class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
    