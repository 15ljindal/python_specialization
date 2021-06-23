import urllib.request, urllib.parse, urllib.error
from twitter_url import augment
import ssl

print('Calling Twitter...')
url = augment('https://api.twitter.com/1.1/statuses/user_timeline.json',
              {'screen_name': 'tithy30', 'count': '5'})
print(f"URL: [{url}]")

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

connection = urllib.request.urlopen(url, context=ctx)
data = connection.read()
print(f"Data: [{data}]")

print ('======================================')
headers = dict(connection.getheaders())
print(f"HEADERS: [{headers}]")
