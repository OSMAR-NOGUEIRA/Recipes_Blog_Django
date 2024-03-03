from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/search/', views.search, name='search'),
    path('recipes/category/<int:category_id>/', views.category, name='category'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]
