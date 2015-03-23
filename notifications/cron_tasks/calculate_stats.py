from django.core.management import call_command


def emit_notices():
    call_command('emit_notices')
