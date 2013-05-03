from django.core.management import call_command

from api.models import EyeHistory

def add_favicons():
    call_command('add_favicons', *EyeHistory.objects.all())