from django import forms


class LoginForm(forms.Form): # Nao herdando de nenhum model e sim de um form model padrao do django para criacao de um formulario personalizado
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your username here',
            'class': 'input-field',
        }),
    )
    password = forms.CharField(
        widget= forms.PasswordInput(attrs={
            'placeholder': 'Type your password here',
            'class': 'input-field',
        }),
    )

    
