from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
    sex_choice = ((0,'Nữ'), (1,'Nam'), (2,'Không xác định'))
    birth = models.DateField(blank=True, null=True)
    sex = models.IntegerField(choices=sex_choice, default=0)
    address = models.CharField(default='', max_length=255)
    
    
    