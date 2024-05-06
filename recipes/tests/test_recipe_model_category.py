from django.core.exceptions import ValidationError

from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(name='Representation Test')
        return super().setUp()
    
    def test_model_recipe_category_max_length(self):
        self.category.name = 'A'*66
        with self.assertRaises(ValidationError):
             self.category.full_clean()

    def test_class_category_str_representation(self):
        needed = 'Testing Representation'
        self.category.name = 'Testing Representation'
        self.category.full_clean()
        self.category.save()
        self.assertEqual(str(self.category), needed)
    