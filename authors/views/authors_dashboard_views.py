from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
from django.utils import timezone

from authors.forms import AuthorRecipeEditForm
from recipes.models import Recipe


PER_PAGE = int(os.environ.get('PER_PAGE', 6))

@login_required(login_url='authors:login', redirect_field_name='next') #faz com que essa pagina so seja acessavel caso o user estaja logado senao sera redirecionado para a pagina de login
def dashboard(request):
    recipes = Recipe.objects.filter(is_published=False, author=request.user).order_by('-updated_at')
    
    context = {
        'page_title':'My Dashboard',
        'recipes':recipes,
    }
    return render(request, 'authors/html/dashboard.html', context)

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_new_recipe(request):
    form = AuthorRecipeEditForm(request.POST or None,
                                files=request.FILES or None, #to make the form work with files(in the case the img of the recipe) // you gotta use the enctype="multipart/form-data" in the form as well 
                                )
    
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        
        recipe.save()
        messages.success(request, 'Recipe created sucesfully!')
        return redirect('authors:dashboard')
        
    context = {
        'page_title':'New Recipe',
        'form': form,
        'form_action':reverse('authors:dashboard_new_recipe'),
    }
    return render(request, 'authors/html/recipe_create.html', context)

@login_required(login_url='authors:login', redirect_field_name='next')
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, is_published=False, author=request.user)
    form = AuthorRecipeEditForm(request.POST or None,
                                instance=recipe,
                                files=request.FILES or None, #to make the form work with files(in the case the img of the recipe) // you gotta use the enctype="multipart/form-data" in the form as well 
                                )
    
    if form.is_valid():
        recipe = form.save(commit=False)
        
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.updated_at = timezone.now()

        recipe.save()
        messages.success(request, 'Your recipe has been saved sucessfully')
        return redirect(reverse('authors:recipe_edit', args=(recipe_id,)))
        
    context = {
        
        'recipe': recipe,
        'form': form,
    }
    return render(request, 'authors/html/dashboard_recipe.html', context)

@login_required(login_url='authors:login', redirect_field_name='next')
def recipe_delete(request):
    if not request.POST:
        raise Http404

    if request.POST:
        recipe_id = request.POST.get('recipe_to_delete')
        recipe = get_object_or_404(Recipe, id=recipe_id, is_published=False, author=request.user)
        recipe.delete()
        messages.success(request, f'Recipe "{recipe.title}" deleted sucessfully!')
        return redirect('authors:dashboard')
    return redirect('authors:dashboard')
    