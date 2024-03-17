from django import forms

from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password', 
            ] 
        
        #you can modify the text of the labels
        labels = {
            'email' : 'E-mail',
        }

        # you can edit the help text of any field
        help_texts = {
            'email': 'The Email must be valid.',
        }

        # you can edit the error_messages of any field
        error_messages = {
            'username': {
                'required': 'This field can not be enpty.',
                'invalid': 'This field is invalid',
            },
            'email': {
                'required': 'This field can not be enpty.',
                'invalid': 'This field is invalid',
            }
        }

        widgets = {
            'username' : forms.TextInput(attrs={
                'placeholder': 'eg: user001',
                'class' : 'input text-input',
            }),
            'password' : forms.PasswordInput(attrs={
                'placeholder' : 'Type your password here',
            })
        }