from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from .managers import UserManager

#Kana sherelle est fabuleuse Courage...

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    pays = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __str__(self):
        return self.email

    
class Question(models.Model):
    anonyme = models.BooleanField(default=True)
    text = models.CharField(max_length=1000, null=False, blank=False )
    created_at = models.DateTimeField(default = timezone.now)
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, related_name = 'questions')
   
class Reponse(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name = 'reponses')#D ACCORD
    verified = models.BooleanField(default=False) #ICI on va verifier les reponses avant de les afficher manuellement
    question = models.ForeignKey(Question, models.CASCADE, related_name = 'reponses')
    reponses = models.CharField(max_length=1000, null=False, blank=False )
    created_at = models.DateTimeField(default = timezone.now)
    vote = models.IntegerField(default = 0)

