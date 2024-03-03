from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404

from recipes.models import Recipe



def index(request):
    recipes = Recipe.objects.order_by('-id').filter(is_published=True)

    context = {
        'recipes' : recipes,
        'page_title': 'Recipes - Home'
    }
    return render(request, 'recipes/html/index.html', context)

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.order_by('-id').filter(category__id=category_id, is_published=True))
    category_title = recipes[0].category.name
    context = {
        'recipes' : recipes,
        'page_title': f'{category_title}'
    }
    return render(request, 'recipes/html/index.html', context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, is_published=True)
    recipe_title = recipe.title
    context = {
        'recipe' : recipe,
        'page_title': f'{recipe_title}',
        'is_detail_page' : True,
    }
    return render(request, 'recipes/html/recipe_detail.html', context)

def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    context = {
        'page_title': f'{search_term} - Recipe Search',
        'search_term': search_term,
    }
    
    return render(request, 'recipes/html/search.html', context)