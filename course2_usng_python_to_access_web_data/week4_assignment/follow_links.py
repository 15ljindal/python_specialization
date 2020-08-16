import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

url = input('Enter URL:')
position = int(input('Enter position to chase:'))
depth = int(input('Enter depth of traversal:'))

name = ""
for i in range(depth):
    # print('TAG:', tag)
    # print('URL:', tag.get('href', None))
    # print('Contents:', ','.join(tag.contents))
    # print('Attrs:', tag.attrs)
    
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    tag = tags[position - 1]

    url = tag.get('href', None)
    name = tag.contents[0]

print(name)
    