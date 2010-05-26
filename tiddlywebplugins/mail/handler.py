"""
entry point for an email coming in

also exit point for sending an email
"""
from utils import EmailAddressError
from response import retrieve_from_store
from put import put_to_store
from subscriptions import make_subscription, delete_subscription

import re

EMAIL_ACTION = {
    'view': retrieve_from_store,
    'post': put_to_store,
    'subscribe': make_subscription,
    'unsubscribe': delete_subscription
}

def handle_email(email):
    """
    take an email, figure out what to do with it, and send a response
    """
    try:
        response_email = EMAIL_ACTION[get_action(email['to'])](email)
    except KeyError:
        raise EmailAddressError('Unsupported email address %s' % email['to'])
    
    return send_email(response_email)

def get_action(email_address):
    """
    determine whether we are posting, viewing or subscribing
    """
    email_address = re.sub('[^\<]*\<([^\>]+)\>',
        lambda match: match.group(1), email_address)
    action = email_address.split("@", 1)[0]

    return action.split('+', 1)[0]

def send_email(mail):
    print 'I dont know how to send email yet. Please implement send_email'
    return mail
