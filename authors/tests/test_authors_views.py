from recipes.tests.test_recipe_base import RecipeTestBase
from django.contrib.auth.models import User
from django.urls import reverse

from authors.views.authors_dashboard_cbv_views import DashboardRecipe, DashboardRecipeDelete
from authors.models import Profile



class AuthorsDashboardViewTest(RecipeTestBase):
    def test_authors_get_recipe__receive_id_none(self):
        r = DashboardRecipe.get_recipe(self, id=None)
        self.assertEqual(r, None)
        
    def test_authors_deleting_recipe_ok(self):
        user = self.make_author(username='User_test', password='My_pass123')
        self.client.login(username=user.username, password='My_pass123')
        recipe = self.make_recipe(author_data=user, is_published=False)
        
        url = reverse('authors:recipe_delete')
        
        response = self.client.post(url, data={'recipe_to_delete':recipe.id}, follow=True)
        
        self.assertIn('Recipe Title&quot; deleted sucessfully.', response.content.decode('utf-8'))
        
        
class AuthorsProfileViewTest(RecipeTestBase):
    def test_authors_profile_view_gets_right_profile_by_the_id_given(self):
        user = self.make_author(username='User_test', password='My_pass123')
        profile = user.profile
        
        profile.bio = 'Testing Profile!'
        profile.save()
        
        url = reverse('authors:profile', kwargs={'id':profile.id})
        response = self.client.get(url)
        self.assertIn('Testing Profile!', response.content.decode('utf-8'))
        
    def test_authors_edit_profile_view_raises_404_if_not_found_profile_id_matching(self):
        user = self.make_author(username='User_test', password='Mypass123@')
        self.client.login(username=user.username, password='Mypass123@')
        
        url = reverse('authors:profile_edit', kwargs={'pk':2})
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)
        
    def test_authors_edit_profile_view_user_can_only_edit_his_own_profile_ok(self):
        user1 = self.make_author(username='User_test01', password='Mypass123@')
        self.client.login(username=user1.username, password='Mypass123@')
        
        user2 = self.make_author(username='User_test02', password='Mypass123@')
        
        url = reverse('authors:profile_edit', kwargs={'pk':user2.profile.id})
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)
        
    def test_authors_edit_profile_view_checks_if_form_is_valid(self):
        user = self.make_author(username='User_test', password='Mypass123@')
        self.client.login(username=user.username, password='Mypass123@')
        
        url = reverse('authors:profile_edit', kwargs={'pk':user.profile.id})

        response = self.client.post(url, data={'bio':''}, follow=True)
        
        self.assertIn('Profile bio can not be empty.', response.content.decode('utf-8'))
        