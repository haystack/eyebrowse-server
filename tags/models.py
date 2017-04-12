from django.db import models
from django.contrib.auth.models import User

# Domain and page objects
class Domain(models.Model):
    name = models.CharField(max_length=100, default='', unique=False)
    url = models.URLField(max_length=300, blank=False, null=False)

class Page(models.Model):
    url = models.URLField(max_length=300, blank=False, null=False)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)

    #from eyehistory
    title = models.CharField(max_length=2000, default='')
    favicon_url = models.TextField(default='')
    favIconUrl = models.URLField(max_length=2000, default='')

    #from popularhistory
    description = models.TextField(default='')
    img_url = models.URLField(max_length=2000, default='')


# Represents a highlighted string in an article
class Highlight(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    highlight = models.CharField(max_length=10000, blank=False, null=False)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)



