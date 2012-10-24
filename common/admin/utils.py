from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings

from email.mime.text import MIMEText
from email_templates import *
import email.utils
import smtplib

import os, sha, re, random

def send_mail(subject, html_content, user_emails, from_email=settings.DEFAULT_EMAIL):
    """
    Email current users
    user_emails is a list of emails to send to.
    """
    #send live mail
    if setttings.DEBUG:
        for to_email in user_emails:

            localSend(subject, html_content, to_email, from_email)
    else:
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, user_emails)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

def send_local_mail(subject, html_content, to_email, from_email=settings.DEFAULT_EMAIL):
    # Create the message
    msg = MIMEText(html_content)
    msg['To'] = email.utils.formataddr(('Recipient', to_email))
    msg['From'] = email.utils.formataddr(('Author', from_email))
    msg['Subject'] = subject

    server = smtplib.SMTP('127.0.0.1', 1025)
    server.set_debuglevel(True) # show communication with the server
    try:
        server.sendmail(from_email, [to_email], msg.as_string())
    finally:
        server.quit()