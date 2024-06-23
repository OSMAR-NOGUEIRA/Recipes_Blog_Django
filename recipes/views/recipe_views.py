from django.db.models.query import QuerySet
from django.http import Http404
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext as _
from django.utils import translation

import os

from recipes.models import Recipe
from utils.pagination import make_pagination
from tag.models import Tag


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name= 'recipes'
    paginate_by = 5
    ordering = ['-id']
    template_name = 'recipes/html/index.html'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        
        qs = qs.select_related('author', 'category',) #Just to improve the performance when getting data from database
        
        #prefetch_related = COMO ESTAMOS USANDO AS TAGS FAZEMOS A RELACAO ENTRE AS RECIPES E TAGS PARA SEREM BUSCADAS NA MESMA CONSULTA NO BANCO DE DADOS, PARA MELHOR PERFORMANCE
        qs = qs.prefetch_related('tags', 'author__profile',)
        
        return qs

    def get_context_data(self, *args, **kwargs):
        recipes = self.get_queryset()
        context = super().get_context_data(*args, **kwargs)
        
        page_obj, pagination_range = make_pagination(
            self.request,
            recipes,
            PER_PAGE
        )
        
        context.update(
            {
            'page_title': f'{_('Home')}',
            'recipes' : page_obj,
            'pagination_range' : pagination_range,
            'html_language': translation.get_language() ,#GETTING THE LANGUAGE USED IN THE NAVEGATOR JUST TO SET THE <html lang="{{ html_language }}"> (NOT USED TO TRANSLATE ANYTHING)
            })
        return context
    

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/html/index.html'
    
    
class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/html/index.html'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        category_id = self.kwargs.get('category_id')
        
        qs = qs.filter(
            category__id=category_id,
        )
        
        if not qs:
            raise Http404
        
        return qs
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_translation_title = _('Category')
        
        context.update({
            'page_title': f'{context.get('recipes')[0].category.name} - { category_translation_title }',
        })
        return context
       
       
class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/html/search.html'
    
    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        qs = super().get_queryset(*args, **kwargs)
        
        qs = qs.filter(
            Q(category__name__icontains=search_term) |
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
            is_published=True,
        )
        
        if not search_term:
            raise Http404
        
        return qs
        
        
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()
        
        context.update({
        'page_title': search_term,
        'search_term': search_term,
        'additional_url_query':f'&q={search_term}',
        })
        return context
    

class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/html/recipe_detail.html'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context.update( {
        'page_title': context['recipe'].title,
        'is_detail_page' : True,
        })
        
        return context
    
class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/html/search.html'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        
        tag_slug = self.kwargs.get('slug', '')
        qs = qs.filter(tags__slug=tag_slug)
        
        return qs
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs.get('slug', '')
        
        tag = Tag.objects.filter(slug=slug).first()
        
        if not tag:
            tag = _('No recipes found!')
        
        context.update({
        'page_title': f'{tag} - Tag',
        })
        return context
    