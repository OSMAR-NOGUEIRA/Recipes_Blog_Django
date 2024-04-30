from django.contrib import admin

from recipes import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',

@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'created_at', 'is_published', 'author', 
    list_display_links = 'title',
    search_fields = 'id', 'description', 'slug', 'preparation_steps'
    list_filter = 'category', 'author', 'is_published', 'preparation_steps_is_html',
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('title',),   #to auto-generate the slug based in the title
    }