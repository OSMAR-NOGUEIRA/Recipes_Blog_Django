from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.utils import translation
from django.utils.translation import gettext as _
from django.urls import reverse
from django.http import Http404
from django.contrib import messages

from authors.forms import AuthorRecipeEditForm, ProfileEditForm
from authors.models import Profile



class ProfileView(TemplateView):
    template_name = 'authors/html/profile.html'
    
    def get(self, request, *args, **kwargs):
        
        context = self.get_context_data(**kwargs)
        profile_id = context.get('id')
        profile = get_object_or_404(Profile.objects.filter(pk=profile_id).select_related('author'), pk=profile_id)
        
        return self.render_to_response({
            **context,
            'profile' : profile,
            'page_title' : f'{_('Profile')}',
            'html_language': translation.get_language(),#GETTING THE LANGUAGE USED IN THE NAVEGATOR JUST TO SET THE <html lang="{{ html_language }}"> (NOT USED TO TRANSLATE ANYTHING)
        })
        

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_edit_profile(request, pk):
    if request.user.profile.id == pk:
        profile = get_object_or_404(Profile, pk=pk)
    else:
        raise Http404
    
    form = ProfileEditForm(
        request.POST or None,
        instance=profile,
        files=request.FILES or None,
        )
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated sucessfully.')
            return redirect('authors:dashboard')
    
    context = {
        'form_action':reverse('authors:profile_edit', kwargs={'pk':pk}),
        'form':form,
        'form_class':'profile-edit-form',
        'page_title':'My profile',
    }
    return render(request, 'authors/html/edit_profile.html', context)
