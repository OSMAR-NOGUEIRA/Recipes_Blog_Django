from django import forms
from recipes.models import Recipe
from django.core.exceptions import ValidationError
from collections import defaultdict #used to create a dict of erros for each field

def is_positive_number(value):
    try:
        number_string = float(value)
    except ValueError:
        return False
    return number_string > 0

class AuthorRecipeEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._my_errors = defaultdict(list)
    
    class Meta:
        model = Recipe
        fields=[
            'cover',
            'title',
            'description',
            'preparation_steps',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
        ]
        
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'title':forms.TextInput(
              attrs={
                  'placeholder':'E.g Onion Rings'
              }  
            ),
            'preparation_steps': forms.Textarea(
                attrs={
                    'placeholder':'Long description of your recipe',
                    'class':'text-area-form-input',
                }
            ),
            'servings': forms.TextInput(
                attrs={
                    'placeholder':'E.g. 12',
                }
            ),
            'preparation_time': forms.TextInput(
                attrs={
                    'placeholder':'E.g. 50',    
                }
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('minutes', 'minutes'),
                    ('Hours', 'Hours'),
                    ('Days', 'Days'),
                )
                ),
            'servings_unit': forms.Select(
                choices=(
                    ('Portions', 'Portions'),
                    ('Pieces', 'Pieces'),
                    ('People', 'People'),
                )
            ),
        }
        
        help_texts = {
            'cover':'You can change the cover selecting another image.',
            'description':'Brief description of your recipe.',
        }
        
        error_messages = {
            'title':{
                'required':'This field is required!',
            }
        }
        
    def clean(self, *args, **kwargs):
        clean = super().clean(*args, **kwargs)
        
        title = clean.get('title')
        description = clean.get('description')
        
        if title == description:
            self._my_errors['title'].append('Title can not be same as description.')
            self._my_errors['description'].append('Description can not be same as title')
        
        if self._my_errors:
            raise ValidationError(self._my_errors)
        
        return clean
        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 4:
            self._my_errors['title'].append('Title must have at least 3 characters.')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            self._my_errors['description'].append('Description must have at least 10 characters.')
        return description
    
    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')
        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append('Preparation time must be a positive number.')
        return preparation_time
    
    def clean_servings(self):
        servings = self.cleaned_data.get('servings')
        if not is_positive_number(servings):
            self._my_errors['servings'].append('Servings must be a positive number.')
        return servings