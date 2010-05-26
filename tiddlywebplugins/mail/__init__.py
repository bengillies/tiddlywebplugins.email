"""
entry point for tiddlywebplugins.mail
"""
from config import config as email_config
from twanager import *

from tiddlyweb.util import merge_config

def init(config):
    """
    initialise email module
    """
    merge_config(config, email_config)
