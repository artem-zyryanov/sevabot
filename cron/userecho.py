import json
import os.path
import random
import urllib
import urllib2

CHAT_ID = '2f5ec32c37ca53bf9aa46ca3098d2629'

messages_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),'userecho_messages')

messages_file = open(messages_filename, 'r')
messages = messages_file.readlines()
messages_file.close()
last_id_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),'userecho_last_id')

last_id = 0
if os.path.isfile(last_id_filename):
    last_id_file = open(last_id_filename, 'r')
    last_id = int(last_id_file.readline())
    last_id_file.close()

API_BASE = 'https://userecho.com/api/v2/forums/16969/topics.json'
TOKEN = 'dbc637997c0c83cb1624a5aa36e94bf878467fa3'
AUTH_PARAMS = '?access_token=' + TOKEN
TOPICS_URL = API_BASE + AUTH_PARAMS + '&filter__id__gt=' + str(last_id)

f = urllib2.urlopen(TOPICS_URL)

result = json.load(f)
if result['status'] == 'success' and result['details']['count'] > 0:
    data = result['data']
    max_id = 0
    max_d = None
    for d in data:
        if d['id'] > max_id:
            max_id = d['id']
            max_d = d
    last_id_file = open(last_id_filename, 'w')
    last_id_file.write(str(max_id))
    last_id_file.close()
    if not max_d is None:
        template = messages[random.randint(0, len(messages) - 1)]
        max_d_description = template.format(description=max_d['description'].encode('utf-8'),
                                            user=max_d['author']['name'].encode('utf-8'),
                                            url=(u'http://elba.userecho.com/topic/'+str(max_d['id'])).encode('utf-8'))
        t = urllib.urlencode({'message': max_d_description, 'chat_id': CHAT_ID})
        r = urllib2.urlopen('http://192.168.76.60:5000/message_unsigned/', t)
        r.read()