from models import *
from django.db.models.signals import post_save
from django.contrib.auth.models import User

def create_user_profile(sender, instance, created, **kwargs):
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance) 

def setup():
    post_save.connect(create_user_profile, sender=User) 
