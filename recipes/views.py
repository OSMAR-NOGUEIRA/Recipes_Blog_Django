from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe



def index(request):
    recipes = Recipe.objects.order_by('-id').filter(is_published=True)

    context = {
        'recipes' : recipes,
    }
    return render(request, 'recipes/html/index.html', context)

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.order_by('-id').filter(category__id=category_id, is_published=True))
    context = {
        'recipes' : recipes,
    }
    return render(request, 'recipes/html/index.html', context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, is_published=True)
    context = {
        'recipe' : recipe,
        'is_detail_page' : True,
    }
    return render(request, 'recipes/html/recipe_detail.html', context)
