"""
functions covering adding a tiddler to the store
"""
from utils import determine_bag

from tiddlyweb.config import config
from tiddlyweb.model.tiddler import Tiddler
from tiddlywebplugins.utils import get_store

def put_to_store(email):
    """
    email is put into store
    """
    store = get_store(config)
    tiddler = Tiddler(email['subject'])
    tiddler.bag = determine_bag(email['to'])
    tiddler.text = email['body']
    toTags, toBase = email['to'].split('@')
    tiddler.tags = toTags.split('+')
    tiddler.tags.remove('post')
    store.put(tiddler)

    response_email = {
        'from': 'view@%s' % toBase,
        'to': email['from'],
        'subject': tiddler.title,
        'body': tiddler.text
    }

    return response_email
