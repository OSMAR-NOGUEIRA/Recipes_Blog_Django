from django.core.exceptions import ValidationError #para tratamento dos dados no cleaned_data
import re



def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$') #expressoes regulares para verificar se a senha vai conter letras de a-z minusculas, letras de A-Z maiusculas, numeros de 0 a 9 e com 8 digitos.

    if not regex.match(password):#se a password nao der match com a expressao regular que criamos assima
        raise ValidationError((
                'Password must have at least one uppercase letter, '
                'one lowercase letter and one number. the length must '
                'be at least 8 characters.'
                ),
                code='invalid',)

def strong_password2(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$') #expressoes regulares para verificar se a senha vai conter letras de a-z minusculas, letras de A-Z maiusculas, numeros de 0 a 9 e com 8 digitos.

    if not regex.match(password):#se a password nao der match com a expressao regular que criamos assima
        raise ValidationError('Type a stronger password.')
