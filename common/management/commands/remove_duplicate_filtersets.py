from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User

from api.models import WhiteListItem, BlackListItem

class Command(NoArgsCommand):
    help = 'Detects and removes duplicated whitelist/blacklist items'
    def handle(self, **options):
        self.stdout.write('Beginning update...\n')
        users = User.objects.all()
        for user in users:
            self._delete_filterset(WhiteListItem, user)
            self._delete_filterset(BlackListItem, user)
            
        self.stdout.write('Update complete.\n')

    def _delete_filterset(self, filterset, user):
        items = filterset.objects.filter(user=user)
        for item in items:
            objs = filterset.objects.filter(user=user, url=item.url)
            if objs.count > 1:
                for obj in objs[1:]:
                    self.stdout.write('Deleting: %s\n'%item)
                    obj.delete()
