from django.db.models.query import QuerySet
from django.http import Http404
from django.db.models import Q
from django.views.generic import ListView, DetailView
import os

from recipes.models import Recipe
from utils.pagination import make_pagination


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListView(ListView):
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
            'page_title': 'Home',
            'recipes' : page_obj,
            'pagination_range' : pagination_range,
            })
        return context
    

class RecipeListViewHome(RecipeListView):
    template_name = 'recipes/html/index.html'
    
    
class RecipeListViewCategory(RecipeListView):
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
        context.update({
            'page_title': context['recipes'][0].category.name,
        })
        return context
       
       
class RecipeListViewSearch(RecipeListView):
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
    

############################################    FUNCTION BASED VIEWS    ##############################################################

#def recipe_detail(request, recipe_id):
#    recipe = get_object_or_404(Recipe, id=recipe_id, is_published=True)
   
#    context = {
#        'recipe' : recipe,
#        'page_title': recipe.title,
#        'is_detail_page' : True,
#    }
#    return render(request, 'recipes/html/recipe_detail.html', context)

#def index(request):
#    recipes = Recipe.objects.order_by('-id').filter(is_published=True,)
    
#    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

#    context = {
#        'page_title': 'Home',
#        'recipes' : page_obj,
#        'pagination_range' : pagination_range,
#    }

#    return render(request, 'recipes/html/index.html', context)

#def category(request, category_id):
#    recipes = get_list_or_404(Recipe.objects.order_by('-id').filter(category__id=category_id, is_published=True))
#    
#    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
#    
#    context = {
#        'recipes' : page_obj,
#        'pagination_range':pagination_range,
#        'page_title': recipes[0].category.name
#    }
#    return render(request, 'recipes/html/index.html', context)


#def search(request):
#    search_term = request.GET.get('q', '').strip()

#    if not search_term:
#        raise Http404()
    
#    recipes = Recipe.objects.filter(
#        Q(title__icontains=search_term) |
#        Q(description__icontains=search_term),
#    ).filter(is_published=True).order_by('-id')

#    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

#    context = {
#        'page_title': search_term,
#        'search_term': search_term,
#        'pagination_range':pagination_range,
#        'recipes': page_obj,
#        'additional_url_query':f'&q={search_term}',
#    }
    
#    return render(request, 'recipes/html/search.html', context)