#! /usr/bin/env python

from django.core.management.base import NoArgsCommand

import smtpd
import asyncore


class Command(NoArgsCommand):
    help = 'Run local mail server'

    def handle(self, **options):
        self.stdout.write('Started server on port 1025\n')
        server = CustomSMTPServer(('127.0.0.1', 1025), None)

        asyncore.loop()

class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message content       :', data
        print 'Message length        :', len(data)
        return
