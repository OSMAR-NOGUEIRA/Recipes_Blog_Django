from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
import os

from recipes.models import Recipe
from utils.pagination import make_pagination_range, make_pagination


PER_PAGE = int(os.environ.get('PER_PAGE', 6))

def index(request):
    recipes = Recipe.objects.order_by('-id').filter(is_published=True,)
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        'page_title': 'Home',
        'recipes' : page_obj,
        'pagination_range' : pagination_range,
    }

    return render(request, 'recipes/html/index.html', context)

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.order_by('-id').filter(category__id=category_id, is_published=True))
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    
    context = {
        'recipes' : page_obj,
        'pagination_range':pagination_range,
        'page_title': recipes[0].category.name
    }
    return render(request, 'recipes/html/index.html', context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, is_published=True)
   
    context = {
        'recipe' : recipe,
        'page_title': recipe.title,
        'is_detail_page' : True,
    }
    return render(request, 'recipes/html/recipe_detail.html', context)

def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(title__icontains=search_term) |
        Q(description__icontains=search_term),
    ).filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        'page_title': search_term,
        'search_term': search_term,
        'pagination_range':pagination_range,
        'recipes': page_obj,
        'additional_url_query':f'&q={search_term}',
    }
    
    return render(request, 'recipes/html/search.html', context)