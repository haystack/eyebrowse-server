from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(NoArgsCommand):
    help = """
    After running the import_db.sh script this sets all
    of the usrs except admins to inactive so that they
    cannot log into the dev site.

    Important!! Only run this on staging server since it will
    mess up the registration process for future users."""

    def handle(self, **options):
        self.stdout.write('Beginning update...\n')
        users = User.objects.all()
        admins = [admin[1] for admin in settings.ADMINS]
        for user in users:
            if user.email not in admins:
                self.stdout.write('Updating %s\n' % user.username)
                user.active = False
                user.set_unusable_password()
                user.save()

        self.stdout.write('Update complete.\n')
