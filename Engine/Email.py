# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import smtplib


def mail(serverURL=None, sender='', to='', subject='', text=''):
    """
    Usage:
    mail('somemailserver.com', 'me@example.com', 'someone@example.com', 'test', 'This is a test')
    """
    headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, to, subject)
    message = headers + text
    mailServer = smtplib.SMTP(serverURL)
    mailServer.sendmail(sender, to, message)
    mailServer.quit()
