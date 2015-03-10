from django.core.management.base import BaseCommand

from api.models import EyeHistory


class Command(BaseCommand):
    args = '<EyeHistory EyeHistory ...>'
    help = 'Fill in missing favicons for the given history objects'

    def handle(self, *args, **options):
        self.stdout.write('Beginning update...\n')

        count = 0
        for arg in args:

            if not count % 100:
                self.stdout.write('Updated %s \n' % count)

            count += 1

            if arg.favIconUrl == "":
                history = EyeHistory.objects.filter(domain=arg.domain)
                for h in history:
                    # found a valid favicon for the domain
                    if h.favIconUrl != "":

                        self.stdout.write('Updated %s \n' % arg)

                        arg.favIconUrl = h.favIconUrl
                        arg.save()
                        break

        self.stdout.write('Update complete.\n')
