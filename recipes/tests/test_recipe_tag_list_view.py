from django.urls import reverse
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase
from utils.generateFakes import make_batch_of_recipes
from tag.models import Tag



class RecipeTagViewTest(RecipeTestBase):
    def test_recipe_tag_list_view_returns_right_recipes(self):
        tag_1 = Tag.objects.create(name='Tag test 01')
        tag_2 = Tag.objects.create(name='Tag test 02')
        
        a, b, c, d = make_batch_of_recipes(qty_recipes=4)
        
        a.tags.add(tag_1)
        b.tags.add(tag_1)
        c.tags.add(tag_1)
        d.tags.add(tag_2)
        
        url = reverse('recipes:tag', kwargs={'slug':tag_1.slug})
        response = self.client.get(url)
        ctx_objs = response.context['recipes'].object_list
        
        self.assertListEqual(
            sorted([a.title, b.title, c.title]),
            sorted([ctx_objs[0].title, ctx_objs[1].title, ctx_objs[2].title])
            )
        self.assertNotIn(d, ctx_objs)
        
    def test_recipe_tag_list_view_display_no_recipes_found_if_none_recipe_matching_the_tag(self):
        url = reverse('recipes:tag', kwargs={'slug':'slug-test'})
        response = self.client.get(url)
        self.assertIn('No recipes found!', response.content.decode())