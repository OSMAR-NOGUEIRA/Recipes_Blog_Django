from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.templatetags.static import static


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    image = models.ImageField(upload_to='profile_imgs/', null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    
    bio = models.TextField(default='', blank=True, verbose_name=_('Bio'))
    
    
    def __str__(self):
        return f"{self.author.username}'s profile"
    
    @property
    def name(self):
        if self.displayname:
            name = self.displayname
        else:
            name = self.user.username
        return name
    
    @property
    def avatar(self):
        try:
            avatar = self.self.image.url
        except:
            avatar = static('global/img/avatar.png')
        return avatar