from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from common.defaults import DEFAULT_WHITELIST, DEFAULT_BLACKLIST
from accounts.models import *
from api.models import WhiteListItem, BlackListItem
from stats.models import FavData

def create_user_profile(sender, instance, created, **kwargs):
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)
       fav_data = FavData.objects.get_or_create(user=instance)
       set_user_perms(instance)

def set_user_perms(user):
    content_types = ['whitelistitem', 'blacklistitem', 'eyehistory']
    mod_types = ['add', 'change', 'delete']
    to_add = [Permission.objects.get(codename="%s_%s"%(mod_type, content)) for mod_type in mod_types for content in content_types]
    [user.user_permissions.add(perm) for perm in to_add]
    user.save()

def add_defaults(user, default_list, filter_set_item):
    for url in default_list:
        item = filter_set_item(user=user, url=url)
        item.save()

def setup():
    post_save.connect(create_user_profile, sender=User)