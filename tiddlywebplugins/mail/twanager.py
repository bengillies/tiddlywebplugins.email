"""
twanager commands
"""
from handler import send_email
from response import make_digest_email

from tiddlyweb.config import config
from tiddlyweb.model.bag import Bag
from tiddlyweb.manage import make_command
from tiddlywebplugins.utils import get_store

@make_command()
def send_subscriptions(args):
    """send subscriptions: Send all subscriptions of the named type (eg daily). <subscription_type>"""
    bag = args[0]
    store= get_store(config)
    bag = store.get(Bag(bag))

    for tiddler in bag.list_tiddlers():
        tiddler = store.get(tiddler)
        mail = make_digest_email(tiddler)
        if mail:
            send_email(mail)

@make_command()
def slurp_email(args):
    """slurp_email: Take a raw email direct from the server on stdin and process it"""
    pass

@make_command()
def check_email(args):
    """check_email: Check for new emails from a POP server and process them."""
    pass
