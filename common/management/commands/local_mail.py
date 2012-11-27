"""
A management command which runs a local mail server with the port specified. Prints the mail content to the terminal allowing for debugging during development. Defaults to port 1025 if no port is given.

"""
from django.core.management.base import BaseCommand

import smtpd
import asyncore


class Command(BaseCommand):
    args = '<port>'
    help = 'Run local mail server'

    def handle(self, *args, **options):
        try:
            port = int(args[0])
        except:
            self.stdout.write('Invalid or no port number given, defaulting to port 1025.\n')
            port = 1025

        self.stdout.write('Started server on port %s\n'%port)
        server = CustomSMTPServer(('127.0.0.1', port), None)

        asyncore.loop()

class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message content       :', data
        print 'Message length        :', len(data)
        return
