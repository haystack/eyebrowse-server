from django.core.management import call_command

def update_popular_history():
    call_command('update_popular_history')
