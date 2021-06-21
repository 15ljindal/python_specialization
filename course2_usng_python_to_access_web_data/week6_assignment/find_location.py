import urllib.request, urllib.parse, urllib.error
import ssl
import json

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"
location = input('Enter location: ')
params = {}
params["address"] = location
params["key"] = "AIzaSyDlem06zAqWLTJNLk9e143gOKl-UW5O7-M"
url = serviceurl + urllib.parse.urlencode(params)

print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read()
print('Retrieved', len(data), 'characters')
# print(data.decode())

jdata = json.loads(data)
# print(json.dumps(jdata, indent=4))
if jdata["status"] == "OK":
    print(f'Place id: {jdata["results"][0]["place_id"]}')
else:
    print(f'ERROR: status is not OK: {jdata["status"]}')