import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# ignore ssl certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# url = input('Enter URL:')
# url = 'http://py4e-data.dr-chuck.net/comments_42.html'
url = 'http://py4e-data.dr-chuck.net/comments_761237.html'
html = urllib.request.urlopen(url).read()
# for line in html.splitlines():
#     line = line.decode()
#     print(line.strip())

soup = BeautifulSoup(html, 'html.parser')

tags = soup('span')
ans = 0
for tag in tags:
    # print('TAG:', tag)
    # print('URL:', tag.get('href', None))
    # print('Contents:', ','.join(tag.contents))
    # print('Attrs:', tag.attrs)
    ans += int(tag.contents[0])

print(ans)