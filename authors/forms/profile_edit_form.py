from django import forms
from django.core.exceptions import ValidationError


from authors.models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'image', 'displayname', 'bio',
        
        widgets = {
            'image': forms.FileInput(),
            'displayname': forms.TextInput(attrs={'placeholder':'Add display name',}),
            'bio': forms.Textarea(attrs={
                'rows':3,
                'placeholder': 'Add information',
            }),
        }