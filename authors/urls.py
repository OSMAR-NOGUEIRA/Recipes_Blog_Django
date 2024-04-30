from django.urls import path

from authors import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/recipe/new/', views.dashboard_new_recipe, name='dashboard_new_recipe'),
    path('dashboard/recipe/<int:recipe_id>/edit/', views.DashboardRecipe.as_view(), name='recipe_edit'),
    path('dashboard/recipe/delete/', views.recipe_delete, name='recipe_delete'),
]
