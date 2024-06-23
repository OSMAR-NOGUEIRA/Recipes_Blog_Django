from django.contrib import admin
from .models import Tag

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'id', 'slug'
    search_fields = 'id', 'name', 'slug'
    list_per_page = 10
    list_editable = 'name',
    ordering = '-id',
    prepopulated_fields = { #USADO PARA UM SE AUTO PREENCHER SEGUINDO OQ VC DIGITOU NO OUTRO CAMPO - NO CASO O SLUG VAI SE AUTO COMPLETAR SEGUINDO OQ VC DIGITARE NO NOME
        'slug' : ('name',),
    }