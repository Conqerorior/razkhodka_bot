import requests
from bs4 import BeautifulSoup

url = 'https://publicbg.mjs.bg/BgInfo/'

req = requests.get(url)
src = req.text


with open('index.html', 'w') as file:
    file.write(src)
