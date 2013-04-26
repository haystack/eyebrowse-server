from stats.models import FavData

from django.core.management import call_command

def user_stat_gen():
    call_command('calculate_favs')