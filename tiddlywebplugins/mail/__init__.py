"""
entry point for tiddlywebplugins.mail
"""
from config import config as email_config
from twanager import send_subscriptions, slurp_email, check_email

from tiddlyweb.manage import merge_config

def init(config):
    """
    initialise email module
    """
    merge_config(config, email_config)
