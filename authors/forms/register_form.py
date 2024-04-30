from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError #para tratamento dos dados no cleaned_data

from utils.django_forms import strong_password, strong_password2


class RegisterForm(forms.ModelForm): #herdando de um Model que no caso vai ser setado na classe Meta 
    first_name = forms.CharField(
          widget=forms.TextInput(attrs={'placeholder': 'e.g. John'}),
          error_messages={'required':'First name is required.',},
          label='First name')
    
    last_name = forms.CharField(
          widget=forms.TextInput(attrs={'placeholder': 'e.g. Conor'}),
          error_messages={'required':'Last name is required.',},
          required=True,
          label='Last name')
    
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. user01+'}),
        help_text=('Username must have letters, numbers or one of those "@.+-_" .'
                   'The length should be between 4 and 150 characters.'),
        error_messages={
            'required' : 'This field can not be empty.',
            'min_length':'Ensure this value has at least 4 characters (it has 3).',
            'max_length':'Ensure this value has at most 150 characters (it has 151).',
            },
        min_length=4, max_length=150,
    )
    
    email = forms.CharField(
          widget=forms.TextInput(attrs={'placeholder': 'e.g. email@email.com'}),
          required=True,
          error_messages={'required':'E-mail is required.',},
          help_text='The Email must be valid.',
          label='E-mail',
                )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty.'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        label='Password',
        validators=[strong_password],)

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password here',
        }),
        error_messages={
            'required': 'Please repeat your password.'
        },
        help_text=
            ('Password must have at least one uppercase letter, '
            'one lowercase letter and one number.'),
        label='Check password',
        validators=[strong_password2],
    )


    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            ] 
    


    def clean(self):
        cleaned_data = super().clean() #pegando o metodo clean da classe pai .  caso nao fazer isso voce pode pegar a password assim: data_password = self.cleaned_data.get('password')


        data_password = cleaned_data.get('password')
        data_password2 = cleaned_data.get('password2')

    
        if data_password2 != data_password:
            raise ValidationError({
                'password2': 'Those passwords didn’t match. Try again.',
                'password': 'Those passwords didn’t match. Try again.',
            },code='invalid',)
        
    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        exists = User.objects.filter(email=email).exists() # checking if alread exists a user with the same email created in the data base

        if exists:
            raise ValidationError('Email is already in use.', code='invalid',)

        return email
    
