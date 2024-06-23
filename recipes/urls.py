from django.urls import path
from recipes import views

app_name = 'recipes'
 
urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='index'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name='category'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
#                     /\
#                     || WE GOT USE PK AS A KEYWORD WHEN USING A DETAIL CLASS BASED VIEW
    path('tags/<slug:slug>/', views.RecipeListViewTag.as_view(), name='tag'),
]