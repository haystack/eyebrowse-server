from django.core.management.base import NoArgsCommand

from api.models import EyeHistory

from common.templatetags.filters import url_domain


class Command(NoArgsCommand):
    help = 'Adds domain field to all EyeHistory'

    def handle(self, **options):
        self.stdout.write('Beginning update...\n')
        history = EyeHistory.objects.all()

        count = 0
        for h in history:
            if not count % 100:
                self.stdout.write('Updated %s \n' % count)

            h.domain = url_domain(h.url)
            h.save()

            count += 1

        self.stdout.write('Update complete.\n')
