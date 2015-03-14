from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User

from live_stream.query_managers import history_search

from stats.models import FavData


class Command(NoArgsCommand):
    help = 'Update favorite objects for all users'

    def handle(self, **options):
        self.stdout.write('Beginning update...\n')
        users = User.objects.all()
        for user in users:
            self._fav_site_calc(user)

        self.stdout.write('Update complete.\n')

    def _fav_site_calc(self, user):
        """
            Helper to compute what the most commonly used
            site is for a given set of history items.
            Returns a url (domain) that is computed
            to be the favorite and the associated favicon
        """

        item_meta = {}

        hist_type, history_items = history_search(
            user, sort="time", filter="", username=user.username)

        if not history_items:
            fav_data, created = FavData.objects.get_or_create(user=user)
            self.stdout.write('Updated user %s, no history.\n' % user.username)
            return

        for item in history_items:

            domain = item.domain

            if domain in item_meta:
                data = item_meta[domain]
                data["count"] += 1
                data["total_time"] += item.total_time
                item_meta[domain] = data
            else:
                item_meta[domain] = {
<<<<<<< HEAD
                    "fav_icon": item.favIconUrl,
                    "count": 1,
                    "total_time": item.total_time,
                    "domain": domain
=======
                    "favicon" : item.favicon_url,
                    "count" : 1,
                    "total_time" : item.total_time,
                    "domain" : domain
>>>>>>> master
                }

        max_count = 0
        max_dict = {}
        for k, v in item_meta.items():
            if v["count"] > max_count:
                max_count = v["count"]
                max_dict = v

        self.stdout.write('Updated user %s, favorite: %s\n' %
                          (user.username, max_dict["domain"]))

        fav_data, created = FavData.objects.get_or_create(user=user)
        fav_data.domain = max_dict["domain"]
        fav_data.favicon_url = max_dict["favicon"]
        fav_data.total_time = max_dict["total_time"]
        fav_data.visit_count = max_dict["count"]
        fav_data.save()
