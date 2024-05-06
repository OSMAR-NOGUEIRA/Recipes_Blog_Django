from django.views import View
from authors.forms import RegisterForm, LoginForm, AuthorRecipeEditForm
from django.utils import timezone
from django.contrib import messages
from recipes.models import Recipe
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch')
class DashboardRecipe(View):
    def get_recipe(self, id=None):
        recipe = None
        if id is not None:
            recipe = get_object_or_404(Recipe, pk=id, is_published=False, author=self.request.user)
        return recipe
    
    def render_recipe(self, form, recipe):
        context = {
            'page_title': f'{recipe.title if recipe else 'New Recipe'}',
            'recipe': recipe,
            'form': form,
        }
        return render(self.request, 'authors/html/dashboard_recipe.html', context)
    
    def get(self, request, recipe_id=None):
        recipe = self.get_recipe(recipe_id)
        form = AuthorRecipeEditForm(instance=recipe,)
        return self.render_recipe(form, recipe)

    def post(self, request, recipe_id=None):
        recipe = self.get_recipe(recipe_id)
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
            return redirect(reverse('authors:recipe_edit', args=(recipe.id,)))
        return self.render_recipe(form, recipe)

@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch')
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe_id = self.request.POST.get('recipe_to_delete')
        recipe = self.get_recipe(recipe_id)
        recipe.delete()
        messages.success(self.request, f'Recipe "{recipe.title}" deleted sucessfully.')
        return redirect('authors:dashboard')