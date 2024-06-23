import string
from random import SystemRandom

from django.db import models
from django.utils.text import slugify
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes.fields import GenericForeignKey



# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            rand_string = ''.join(
                SystemRandom().choices(string.ascii_letters+string.digits, k=5) # CRIANDO UMA STRING ALEATORIA DE 5 CARACTERES PARA SER ADICIONADA AO FINAL DE CADA SLUG 
            )
            self.slug = slugify(f'{self.name}-{rand_string}')
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    
'''                                                   # USING CONTENTTYPE WITH GENERIC RELATION
    #SETANDO AS CONFIGURACOES DO MODEL PARA FUNCIONAR COMO UMA GENERIC RELATION - QUE SERIA UMA MODEL QUE QUALQUER APP POSSA TER RELACAO 
                                                    #INICIO GENERIC RELATION
    
    #REPRESENTA O MODEL QUE QUEREMOS ENCAIXAR AQ
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    
    #REPRESENTA O ID DA LINHA DO MODEL DESCRITO ACIMA 
    object_id = models.CharField(max_length=255)
    
    #UM CAMPO QUE REPRESENTA A RELACAO GENERICA QUE CONHECE OS CAMPOS ACIMA( content_type e objects_id)
    content_object = GenericForeignKey('content_type', 'object_id') 
    
                                                    #FINAL GENERIC RELATION
                             '''             
                                                    