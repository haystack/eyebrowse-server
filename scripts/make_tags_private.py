import setup_django
from tags.models import Tag


def make_tags_private():
  tags = Tag.objects.all()

  for tag in tags:
    if tag.common_tag is not None:
      tag.is_private = False
      tag.save()

if __name__ == '__main__':
  make_tags_private()
