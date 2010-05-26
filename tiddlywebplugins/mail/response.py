"""
code to construct emails ready to send out
"""

def retrieve_from_store(email):
    """
    get the tiddler requested by the email from the store 
    and return it as an email
    """
    store = get_store(config)
    tiddler_title = clean_subject(email['subject'])
    tiddler = Tiddler(tiddler_title)
    bag = determine_bag(email['to'])
    tiddler.bag = bag
    
    try:
        tiddler = store.get(tiddler)
        response_text = tiddler.text
    except NoTiddlerError:
        #Tiddler not found. Return a list of all tiddlers
        bag = Bag(bag)
        bag = store.get(bag)
        response_text = 'The following tiddlers are in %s:\n' % email['to'].split('@')[1]
        tiddlers = bag.gen_tiddlers()
        tiddlers = [tiddler for tiddler in tiddlers]
        response_text += '\n'.join([tiddler.title for tiddler in tiddlers])

    response_email = {
        'from': email['to'],
        'to': email['from'],
        'subject': tiddler.title,
        'body': response_text
    }
    
    return response_email

def make_digest_email(tiddler,environ={}):
    mail_to_send = False
    email_addresses = tiddler.text.splitlines()
    url_suffix = tiddler.title +'.atom'
    now = datetime.datetime.now()
    nowstr = now.strftime('%Y%m%d%H%M%S')
    try:
        before = tiddler.fields['last_generated']
    except KeyError:
        before = '19000220000000' #select a date wayyyyy in the past
    qs = '?select=modified:>%s'%(before) #filter just the changes
    try:
        prefix = config['server_prefix']
    except KeyError:
        prefix = ''
    try:
        host_details = config['server_host']
        try:
            scheme = host_details['scheme']+'://'
            if scheme == 'file://':
                qs = ''
                scheme = ''
        except KeyError:
            scheme=''
        try:
            host = host_details['host']
        except KeyError:
            host=''
        try:
            port =  ':'+host_details['port']
        except KeyError:
            port =''
    except KeyError:
        host = ''
        scheme = ''
        port = ''
    base_feed_url= '%s%s%s%s/%s'%(scheme,host,port,prefix,url_suffix)
    feed_url ='%s%s'%(base_feed_url,qs)
    print feed_url
    feed = feedparser.parse(feed_url)  
    entries = feed.entries
    if len(entries) == 0:
        print 'no activity on this feed'
        return False
    
    subject = 'Email Digest: %s' % feed['feed']['title']
    htmlbody = u'<html><div>note you can <a href="%s">subscribe to this feed via atom feed</a></div>' % base_feed_url
    body = u'''note you can subscribe to this feed via atom feed <%s>

''' % base_feed_url
    for entry in entries:
        if 'summary' not in entry:
            entry['summary'] = ''
        if 'title' not in entry:
            entry['title'] = ''
        if 'link' not in entry:
            entry['link'] = ''
        body += '''%s <%s>
%s

''' % (entry['title'],entry['link'],entry['summary'])
    htmlbody += u'<div><a href="%s"><h1>%s</h1></a>%s</div>'%(entry['link'],entry['title'],entry['summary'])
    htmlbody += u'</html>'

    if email_addresses:
        mail_to_send = {'bcc':email_addresses,'subject':subject,'body':body,'bodyhtml':htmlbody,'from':'ben.gillies@bt.com'}
    else:
        mail_to_send = False
  
    tiddler.fields['last_generated'] = nowstr#add timestamp
    store = get_store(config)
    store.put(tiddler)
    return mail_to_send
