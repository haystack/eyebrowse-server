from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User

from api.models import EyeHistory

class Command(NoArgsCommand):
    help = 'Detects and removes duplicated history entries'
    def handle(self, **options):
        self.stdout.write('Beginning update...\n')
        users = User.objects.all()
        for user in users:
            self._delete_dup_history(user)
            
        self.stdout.write('Update complete.\n')

    def _delete_dup_history(self, user):
        items = EyeHistory.objects.filter(user=user)
        for item in items:
            objs = EyeHistory.objects.filter(user=user, url=item.url, domain=item.domain, title=item.title, total_time=item.total_time, src=item.src)
            if objs.count > 1:
                for obj in objs[1:]:
                    self.stdout.write('Deleting: %s\n'%item)
                    obj.delete()
