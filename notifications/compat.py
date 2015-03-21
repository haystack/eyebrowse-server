import django

from django.conf import settings


# Django 1.5 add support for custom auth user model
if django.VERSION >= (1, 5):
    AUTH_USER_MODEL = settings.AUTH_USER_MODEL
else:
    AUTH_USER_MODEL = "auth.User"


def old_get_user_model():
    return User

try:
    from django.contrib.contenttypes.generic import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.fields import GenericForeignKey  # noqa

try:
    import importlib
except ImportError:
    from django.utils import importlib  # noqa

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = old_get_user_model

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote  # noqa

try:
    from threading import get_ident
except ImportError:
    from thread import get_ident  # noqa

try:
    from account.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required  # noqa

try:
    from django.apps import apps as django_apps
    get_model = django_apps.get_model
except ImportError:
    from django.db.models import get_model as old_get_model  # noqa

    def get_model(path):
        return old_get_model(*path.split("."))
