# Generated by Django 5.0.2 on 2024-05-12 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_category_alter_recipe_cover_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(),
        ),
    ]
