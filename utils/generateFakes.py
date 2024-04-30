
import os
import sys
from datetime import datetime
from pathlib import Path
from random import choice
import random

import django
from django.conf import settings
from django.contrib.auth.models import User

from faker import Faker
from faker_food import FoodProvider

DJANGO_BASE_DIR = Path(__file__).parent.parent


sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False

django.setup()

def make_author(
            username='user',
            first_name='name_1',
            last_name='name_2',
            password='12345678',
            email='a@email.com',
            ):
        
        return User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )

def make_batch_of_recipes(qty_recipes=10, one_recipe_title=None, title_for_all_recipes=None, category=None):
        NUMBER_OF_OBJECTS = qty_recipes


        from recipes.models import Category, Recipe

        fake = Faker()
        fake.add_provider(FoodProvider)

        if category is None:
            categories = ['breakfast', 'sweets', 'soup', 'cakes']
        else:
            categories = [category]

        django_categories = [Category(name=name) for name in categories]
        for category in django_categories:
            category.save()

        author = make_author(username='UserTest')
                  
        django_itens_recipes = []

        for i in range(NUMBER_OF_OBJECTS):
            if i == 1:
                if one_recipe_title != None:
                    title = one_recipe_title
            else:
                title = fake.dish() if title_for_all_recipes == None else title_for_all_recipes
            description = fake.sentence()
            slug = f'{fake.word()}-{fake.word()}-{fake.word()}'
            preparation_time = random.randint(6, 19)
            preparation_time_unit = 'Minutes'
            servings = random.randint(6, 19)
            servings_unit = 'Portions'
            preparation_steps = fake.paragraphs(nb=10)
            preparation_steps_is_html = False
            is_published = True
            category = choice(django_categories)
            
            django_itens_recipes.append(
            Recipe(
                    title=title,
                    description=description,
                    slug=slug,
                    preparation_time=preparation_time,
                    preparation_time_unit=preparation_time_unit,
                    servings=servings,
                    servings_unit=servings_unit,
                    preparation_steps=preparation_steps,
                    preparation_steps_is_html=preparation_steps_is_html,
                    is_published=is_published,
                    category=category,
                    author=author,
                    )
            )

        if len(django_itens_recipes) > 0:
            return Recipe.objects.bulk_create(django_itens_recipes)