from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
#from django.contrib.contenttypes.fields import GenericRelation
import os
from django.conf import settings
from PIL import Image

from tag.models import Tag


IMG_ROOT = os.environ.get('IMG_ROOT', '')

class Category(models.Model):
    name = models.CharField(max_length=65, verbose_name=_('Name'))

    def __str__(self) -> str:
        return self.name

class RecipeManager(models.Manager):    #CREATING OUR OWN MANAGER CLASS
    def get_published_recipes(self):
        return self.filter(is_published=True)

class Recipe(models.Model):
    #SUBSCRIBING THE OBJECTS MANAGER TO USE OUR OWN MANAGER CLASS
    objects = RecipeManager()
    
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165, verbose_name=_('Description'))
    slug = models.SlugField(verbose_name=_('Slug'))
    preparation_time = models.IntegerField(verbose_name=_('Preparation time'))
    preparation_time_unit = models.CharField(max_length=65, verbose_name=_('Preparation time unit'))
    servings = models.IntegerField(verbose_name=_('Servings'))
    servings_unit = models.CharField(max_length=65, verbose_name=_('Servings unit'))
    preparation_steps = models.TextField( verbose_name=_('Preparation steps'))
    preparation_steps_is_html = models.BooleanField(default=False, verbose_name=_('Preparation steps is html'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Upgraded at'))
    is_published = models.BooleanField(default=False, verbose_name=_('Is published'))
    cover = models.ImageField(upload_to=IMG_ROOT, blank=True, default='', verbose_name=_('Cover'))

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None, verbose_name=_('Category'))

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('Author'))

    tags = models.ManyToManyField(Tag, blank=True, default='', verbose_name=_('Tags')) #FAZENDO A RELACAO ENTRE O APP tags COMO UMA manytomany relation

  
    #tags = GenericRelation(Tag, related_query_name='recipes')  #FAZENDO A RELACAO ENTRE O APP tags COMO UMA RELACAO GENERICA
    
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', args=(self.id,))
    
    @staticmethod
    def resize_image(image, new_width, force=False):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size
        
        if original_width <= new_width and force == False:
            image_pillow.close()
            return
        
        new_heigth = int((new_width * original_height) / original_width)
        
        
        new_image = image_pillow.resize((new_width, new_heigth), Image.LANCZOS)
        
        new_image.save(image_full_path, optimize=True, quality=60)
        
        
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'.capitalize()
            self.slug = slug
        
        saved = super().save(*args, **kwargs)
        
        if self.cover:
            try:
                self.resize_image(self.cover, 840)
            except FileNotFoundError:
                ...
                
        return saved
    
    
    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')