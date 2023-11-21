from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    

    
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
   
    
    def __str__(self):
        return self.username