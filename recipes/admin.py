from django.contrib import admin

from recipes import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name', 'id',

@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'title', 'id',