import setup_django
import json
from tags.models import CommonTag, TagCollection
from django.contrib.auth.models import User

def make_tags_private():
  tags = Tag.objects.all()

  for tag in tags:
    if tag.name is not None:
      tag.is_private = True
      tag.save()

if __name__ == '__main__':
  make_tags_private()
