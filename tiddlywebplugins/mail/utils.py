"""
helper functions and classes
"""
from tiddlyweb.config import config

import re
from string import Template


class EmailAddressError(Exception):
    pass

def determine_bag(email_address, config):
    """
    function to map email address to bag name
    """
    try:
        full_domain = email_address.split("@", 1)[1]
    except KeyError:
        raise EmailAddressError('Invalid email address: %s' % email_address)

    host = config['server_host']['host'].lstrip('www.')
    bag_sub = full_domain.rstrip(host)
    bag_template = Template(config['email']['bag_mapping'])
    bag_name = bag_template.safe_substitute(bag=bag_sub)

    return bag_name

def clean_subject(subject):
    """
    remove RE: and FWD: from the subject
    """
    regex = '^(?:(?:RE\: ?)|(?:FWD: ?))+'
    return re.sub(regex, '', subject)
