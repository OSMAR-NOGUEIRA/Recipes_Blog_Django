from django import forms

class PasswordResetForm(forms.Form):
    old_password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder': 'Type your last password here.',
        'class': 'input-field',
        }),
        label='Old password',
        )
    new_password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder': 'Type your new password here.',
        'class': 'input-field',
        }),
        label='New password',
        )
    new_password_confirmation = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder': 'Confirm your new password here.',
        'class': 'input-field',
        }),
        label='New password confirmation',
        )


class FindUserOrEmailForm(forms.Form):
    email_or_username = forms.CharField(
        label='Username or E-mail:',
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