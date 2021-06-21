import urllib.request, urllib.parse, urllib.error
import ssl
import json

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter location: ')
if len(url) < 1:
    exit()

print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)

data = uh.read()
print('Retrieved', len(data), 'characters')
# print(data.decode())
jdata = json.loads(data)
commentsCount = 0
totalSum = 0
for comment in jdata["comments"]:
    commentsCount += 1
    totalSum += int(comment["count"])

print(f"Count: {commentsCount}")
print(f"Sum: {totalSum}")