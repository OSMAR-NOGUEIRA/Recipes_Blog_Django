from django.views import View
from authors.forms import RegisterForm, LoginForm, AuthorRecipeEditForm
from django.utils import timezone
from django.contrib import messages
from recipes.models import Recipe
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


class DashboardRecipe(View):
    def get_recipe(self, id):
        recipe = None
        if id:
            recipe = get_object_or_404(Recipe, pk=id, is_published=False, author=self.request.user)
        return recipe
    
    def render_recipe(self, form, recipe):
        context = {
            'page_title': f'{recipe.title}',
            'recipe': recipe,
            'form': form,
        }
        return render(self.request, 'authors/html/dashboard_recipe.html', context)
    
    def get(self, request, recipe_id):
        recipe = self.get_recipe(recipe_id)
        form = AuthorRecipeEditForm(instance=recipe,)
        return self.render_recipe(form, recipe)
        

    def post(self, request, recipe_id):
        recipe = self.get_recipe(recipe_id)
        form = AuthorRecipeEditForm(request.POST or None,
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
        return self.render_recipe(form, recipe)