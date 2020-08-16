import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl


url = input('Enter URL: ')
uh = None
if url.startswith('https'):
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    uh = urllib.request.urlopen(url, context=ctx)
else:
    uh = urllib.request.urlopen(url)

data = uh.read()

tree = None
try:
    tree = ET.fromstring(data)
except:
   print('ERROR: Could not read xml correctly')
   print(data)
   assert(0)

comments = tree.findall('comments/comment')
ans = 0
for c in comments:
    values = c.findall('count')
    for v in values:
        t = v.text
        ans += int(t)

print(ans)
