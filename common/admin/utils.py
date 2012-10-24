from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings

from email_templates import *

import os, sha, re, random

def emailUsers(subject, html_content, user_emails, from_email='eyebrowse@mit.edu'):
    """
    Email current users
    user_emails is a list of emails to send to.
    """
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, user_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()