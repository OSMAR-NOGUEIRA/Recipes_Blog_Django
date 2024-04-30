from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os

from authors.forms import RegisterForm, LoginForm


PER_PAGE = int(os.environ.get('PER_PAGE', 6))

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    
    form = RegisterForm(register_form_data)

    context = {
        'page_title': 'Register',
        'form': form,
        'form_action': reverse('authors:register_create'),
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

        messages.success(request, 'User created sucessfully! Please log in.')
        del(request.session['register_form_data'])
        return redirect('authors:login')  

    return redirect('authors:register')

def login_view(request):
    form = LoginForm()

    context = {
        'page_title': 'Login',
        'form': form,
        'form_action': reverse('authors:login_create'),
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
            messages.success(request, 'You are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials.')
    
    else:
        messages.error(request, 'Invalid username or password.')

    return redirect(reverse('authors:dashboard'))

@login_required(login_url='author:login', redirect_field_name='next') #faz com que essa pagina so seja acessavel caso o user estaja logado senao sera redirecionado para a pagina de login
def logout_view(request):
    if not request.POST:
        messages.error(request,'Invalid logout request!')
        return redirect(reverse('authors:login'))
    
    if request.POST.get('username') != request.user.username:  #SE O USUARIO QUE FOI RECEBIDO NO POST NAO E' O MESMO QUE ESTA LOGADO
        messages.error(request,'Invalid logout User!')
        return redirect(reverse('authors:login'))

    logout(request) # User logouting
    messages.success(request, 'Logged out sucessfully.')
    return redirect(reverse('authors:login'))
