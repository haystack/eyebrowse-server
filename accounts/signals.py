from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save

from accounts.models import UserProfile

from stats.models import FavData


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
        FavData.objects.get_or_create(user=instance)
        set_user_perms(instance)


def set_user_perms(user):
    content_types = [
        'whitelistitem', 'blacklistitem', 'eyehistory', 'chatmessage']
    mod_types = ['add', 'change', 'delete']
    to_add = [Permission.objects.filter(
        codename="%s_%s" % (mod_type, content))[0]
        for mod_type in mod_types for content in content_types]
    [user.user_permissions.add(perm) for perm in to_add]
    user.save()


def add_defaults(user, default_list, filter_set_item):
    for url in default_list:
        item = filter_set_item(user=user, url=url)
        item.save()


def setup():
    post_save.connect(create_user_profile, sender=User)
