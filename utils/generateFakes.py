"""
    project_name = project
    app = recipes
    model_1 = Recipe
    model_2 = category
"""


import os
import sys
from datetime import datetime
from pathlib import Path
from random import choice
import random

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 5

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    from faker import Faker
    from faker_food import FoodProvider

    from faker_file.providers.png_file import GraphicPngFileProvider
    FAKER_IMG = Faker()
    FAKER_IMG.add_provider(GraphicPngFileProvider)
    

    from recipes.models import Category, Recipe

    fake = Faker()
    fake.add_provider(FoodProvider)

    categories = ['breakfast', 'sweets', 'soup', 'cakes']

    django_categories = [Category(name=name) for name in categories]

    for category in django_categories:
        category.save()

    django_itens_recipes = []

    for _ in range(NUMBER_OF_OBJECTS):
        title = fake.dish()
        description = fake.sentence()
        slug = f'{fake.word()}-{fake.word()}-{fake.word()}'
        preparation_time = random.randint(6, 19)
        preparation_time_unit = 'Minutes'
        servings = random.randint(6, 19)
        servings_unit = 'Portions'
        preparation_steps = fake.paragraphs(nb=10)
        preparation_steps_is_html = False
        is_published = True
        cover = jpeg_file = FAKER_IMG.graphic_png_file(size=(800, 800))
        category = choice(django_categories)
        author = f'{fake.name()} {fake.last_name()}'

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
                cover=cover,
                category=category,
                )
        )

    if len(django_itens_recipes) > 0:
     Recipe.objects.bulk_create(django_itens_recipes)