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
    path('dashboard/recipe/new/', views.DashboardRecipe.as_view(), name='dashboard_new_recipe'),
    path('dashboard/recipe/<int:recipe_id>/edit/', views.DashboardRecipe.as_view(), name='recipe_edit'),
    path('dashboard/recipe/delete/', views.DashboardRecipeDelete.as_view(), name='recipe_delete'),
    path('profile/<int:id>', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', views.dashboard_edit_profile, name='profile_edit'),
    path('account/password/reset/step-1/', views.find_email_to_reset_pswrd, name='password_reset_step_1'),
    path('account/password/reset/step-2/', views.reset_password_view, name='password_reset_step_2'),
]
