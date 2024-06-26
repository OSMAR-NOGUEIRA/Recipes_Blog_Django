from recipes.models import Recipe
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os

from recipes.models import Recipe


def delete_cover(instance): 
    try:
         os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...

#QUANDO VOCE APAGAR A RECEITA A IMAGEM TAMBEM VAI SER APAGADA DO SERVIDOR       
@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    delete_cover(old_instance)

#QUANDO VOCE ATUALIZAR A RECEITA A IMAGEM ANTIGA VAI SER APAGADA DO SERVIDOR     
@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    
    if not old_instance:
        return
    
    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)