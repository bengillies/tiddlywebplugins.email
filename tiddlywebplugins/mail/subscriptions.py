"""
functions related to hanlding subscriptions
"""
from tiddlyweb.config import config
from tiddlyweb.store import NoTiddlerError
from tiddlywebplugins.utils import ensure_bag, get_store

from string import Template

SUPPORTED_SUBSCRIPTIONS = [
    'daily',
    'weekly',
    'hourly',
    'monthly'
]

def get_subscriptions_bag(store, subscription_type):
    """
    determine the correct bag requested for the subscription
    """
    sub_template = Template(config['email']['subscription_format'])
    if subscription_type in SUPPORTED_SUBSCRIPTIONS:
        sub_bag = sub_template.safe_substitute(subscription=sub_type)
    else:
        sub_bag = sub_template.safe_substitute(
            subscription=config['email']['default_subscription'])

    ensure_bag(sub_bag, store)

    return sub_bag

def delete_subscription(email):
    """
    remove somebody from a particular subscription
    """
    store = get_store(config)
    recipe = determine_bag(email['to'])
    fromAddress = email['from']  
    subscription_bag = get_subscriptions_bag(store)

    try:
        subscribers_tiddler = store.get(Tiddler('bags/%s/tiddlers' % recipe, subscription_bag))
        subscriber_emails = subscribers_tiddler.text.splitlines()
        try:
            subscriber_emails.remove(fromAddress)
        except ValueError:
            pass

        subscribers_tiddler.text = '\n'.join(subscriber_emails)
        store.put(subscribers_tiddler)
    except NoTiddlerError:
        pass
  
    return {'from': email['to'],
        'to': email['from'],
        'subject': 'You have been unsubscribed from %s' % recipe,
        'body': 'Harry the dog is currently whining in sadness.'
    }
  
      
def make_subscription(email):
    """
    add somebody to a subscription
    """
    store = get_store(config)
    recipe = determine_bag(email['to'])
    fromAddress = email['from']
    subscription_bag = get_subscriptions_bag(store)
    subscribers_tiddler = Tiddler('bags/%s/tiddlers' % recipe, subscription_bag)
    try:
        subscribers_tiddler = store.get(subscribers_tiddler)
        subscriber_emails = subscribers_tiddler.text.splitlines()
        if fromAddress not in subscriber_emails:
            subscriber_emails.append(fromAddress)
        subscribers_tiddler.text = '\n'.join(subscriber_emails)
        store.put(subscribers_tiddler)
    except NoTiddlerError:
        subscribers_tiddler.text = fromAddress 
        store.put(subscribers_tiddler)

    return {'from': email['to'],
        'to': email['from'],
        'subject': 'You have subscribed to %s' % recipe,
        'body': 'You will now receive daily digests. To unsubscribe please email unsubscribe@%s'
    }
