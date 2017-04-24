from django.db import models
from django.contrib.auth.models import User

from api.models import Page, Domain

# Represents a highlighted string in an article
class Highlight(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    highlight = models.CharField(max_length=10000, blank=False, null=False)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

class TagCollection(models.Model):
    name = models.CharField(max_length=80, blank=False, null=False)
    trie_blob = models.TextField(blank=False, null=False)
    subscribers = models.ManyToManyField(User)

class CommonTag(models.Model):
    name = models.CharField(max_length=80, blank=False, null=False)
    color = models.CharField(max_length=10, blank=False, null=False)
    description = models.CharField(max_length=10000, default='')
    tag_collection = models.ForeignKey(TagCollection, on_delete=models.CASCADE, blank=True, null=True)
    subscribers = models.ManyToManyField(User)

class Tag(models.Model):
    name = models.CharField(max_length=80, blank=False, null=False)
    color = models.CharField(max_length=10, blank=False, null=False)
    domain = models.URLField(max_length=300, default='')
    description = models.CharField(max_length=10000, default='')
    is_private = models.BooleanField(default=False)
    position = models.SmallIntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="creator")

    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
    domain_obj = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)

    highlight = models.ForeignKey(Highlight, null=True, on_delete=models.CASCADE)
    
    common_tag = models.ForeignKey(CommonTag, on_delete=models.CASCADE, null=True, blank=True)
    tag_collection = models.ForeignKey(TagCollection, on_delete=models.CASCADE, blank=True, null=True)
    subscribers = models.ManyToManyField(User, related_name="subscribers")


class Vote(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE) # one valuetag to many votes
    voter = models.ForeignKey(User, null=False, blank=False) 


class UserTagInfo(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=False)

