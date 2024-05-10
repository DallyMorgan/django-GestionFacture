from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    
    

    
    avatar = models.ImageField("photo de profil", upload_to='avatars/', blank=True, null=True)
    
   
   
    
    def __str__(self):
        return self.nom
    
    class meta:

        db_table = "Utilisateur"
        verbose_name_plural = "Utilisateurs"