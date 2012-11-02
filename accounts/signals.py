from django.db.models.signals import post_save
from django.contrib.auth.models import User
from common.defaults import DEFAULT_WHITELIST, DEFAULT_BLACKLIST


def create_user_profile(sender, instance, created, **kwargs):
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance) 

def set_default_filterset(sender, instance, created, **kwargs):
    if created:
        add_defaults(instance, DEFAULT_WHITELIST, WhiteListItem)
        add_defaults(instance, DEFAULT_BLACKLIST, BlackListItem)

def add_defaults(user, default_list, filter_set_item):
    for url in default_list:
        item = filter_set_item(user=user, url=url)
        item.save()

def setup():
    post_save.connect(create_user_profile, sender=User) 
