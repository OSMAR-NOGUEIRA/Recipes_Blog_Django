from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.utils import translation
from django.contrib.auth.models import User
from django.db.models import Q
import os

from authors.forms import RegisterForm, LoginForm, PasswordResetForm, FindUserOrEmailForm


PER_PAGE = int(os.environ.get('PER_PAGE', 6))

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    
    form = RegisterForm(register_form_data)
    
    context = {
        'page_title': f'{ _('Register') }',
        'form': form,
        'form_action': reverse('authors:register_create'),
        'html_language': translation.get_language(),#GETTING THE LANGUAGE USED IN THE NAVEGATOR JUST TO SET THE <html lang="{{ html_language }}"> (NOT USED TO TRANSLATE ANYTHING)
    }
    return render(request, 'authors/html/register_view.html', context)

def register_create(request):
    if not request.POST:
        raise Http404()
    
    request.session['register_form_data'] = request.POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password) #precisamos criptografar a password antes de salvar no banco de dados 

        user.save()

        messages.success(request, f'{_('User created sucessfully! Please log in.')}')
        del(request.session['register_form_data'])
        return redirect('authors:login')  

    return redirect('authors:register')

def login_view(request):
    form = LoginForm()
    
    context = {
        'page_title': f'{_('Login')}',
        'form': form,
        'form_action': reverse('authors:login_create'),
        'html_language': translation.get_language(),#GETTING THE LANGUAGE USED IN THE NAVEGATOR JUST TO SET THE <html lang="{{ html_language }}"> (NOT USED TO TRANSLATE ANYTHING)
    }
    return render(request, 'authors/html/login.html', context)

def login_create(request):
    if not request.POST:
        raise Http404
    
    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate( # authenticate checa se as credenciais do usuario estao na base de dados e retorna um booleano
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            messages.success(request, f'{_('You are logged in.')}')
            login(request, authenticated_user)
        else:
            messages.error(request, f'{_('Invalid credentials.')}')
    
    else:
        messages.error(request, f'{_('Invalid username or password.')}')

    return redirect(reverse('authors:dashboard'))

@login_required(login_url='authors:login', redirect_field_name='next') #faz com que essa pagina so seja acessavel caso o user estaja logado senao sera redirecionado para a pagina de login
def logout_view(request):
    if not request.POST:
        messages.error(request, f'{_('Invalid logout request!')}')
        return redirect(reverse('authors:login'))
    
    if request.POST.get('username') != request.user.username:  #SE O USUARIO QUE FOI RECEBIDO NO POST NAO E' O MESMO QUE ESTA LOGADO
        messages.error(request, f'{_('Invalid logout User!')}')
        return redirect(reverse('authors:login'))

    logout(request) # User logouting
    messages.success(request, f'{_('Logged out sucessfully.')}')
    return redirect(reverse('authors:login'))

def find_email_to_reset_pswrd(request):
    form = FindUserOrEmailForm()
    
    if request.method == 'POST':
        form = FindUserOrEmailForm(request.POST)
        data = form['email_or_username'].data
        user = get_object_or_404(User,
                                 Q(username__icontains=data) |
                                 Q(email__icontains=data),)
        ...
    
    context = {
        'form_action': reverse('authors:password_reset_step_1'),
        'form':form,
    }
    return render(request, 'authors/html/email_search.html', context)

def reset_password_view(request):
    form = PasswordResetForm()
    
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        data = form['new_password'].data
    
    context = {
        'form': form,
        'form_action': reverse('authors:password_reset'),
    }
    return render(request, 'authors/html/update_password.html', context)