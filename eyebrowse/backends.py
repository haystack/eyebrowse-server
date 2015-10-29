from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailOrUsernameBackend(ModelBackend):

  def authenticate(self, username=None, password=None):
    try:
      kwargs = {'email': username}
      user = User.objects.get(**kwargs)
    except:
      kwargs = {'username': username}
      user = User.objects.get(**kwargs)
    finally:
      try:
        if user.check_password(password):
          return user
      except:
        # Run the default password hasher once to reduce the timing
        # difference between an existing and a non-existing user.
        User.set_password(password)
        return None
