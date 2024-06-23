from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from django.utils import timezone
from django.utils import translation
from django.utils.translation import gettext as _


from recipes.models import Recipe
from authors.models import Profile

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

@login_required(login_url='authors:login', redirect_field_name='next') #faz com que essa pagina so seja acessavel caso o user estaja logado senao sera redirecionado para a pagina de login
def dashboard(request):
    recipes = Recipe.objects.filter(is_published=False, author=request.user).order_by('-updated_at')
    
    context = {
        'page_title':f'{_('My Dashboard')}',
        'recipes':recipes,
        'html_language': translation.get_language(),#GETTING THE LANGUAGE USED IN THE NAVEGATOR JUST TO SET THE <html lang="{{ html_language }}"> (NOT USED TO TRANSLATE ANYTHING)
    }
    return render(request, 'authors/html/dashboard.html', context)