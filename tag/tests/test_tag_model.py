from django.test import TestCase
from tag.models import Tag


class TagModelTest(TestCase):
    def test_method_save_create_a_slug_of_title_and_a_random_string_for_the_field_itself_if_no_slug_passed(self):
        tag1 = Tag.objects.create(name='Tag test')
        tag2 = Tag.objects.create(name='Tag test')
        
        slug_test = 'slug-test-exemple-02'
        tag3 = Tag.objects.create(name='Tag test', slug=slug_test)
        
        self.assertNotEqual(tag1.slug, tag2.slug)
        self.assertGreaterEqual(14, len(tag1.slug))
        self.assertEqual(tag3.slug, slug_test)
        