import requests
from bs4 import BeautifulSoup
#
# url = 'https://publicbg.mjs.bg/BgInfo/'
#
# req = requests.get(url)
# src = req.text
#
#
# with open('index.html', 'w') as file:
#     file.write(src)
with open('index.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'html.parser')

forms = soup.find_all(class_='control-label')
print(forms)

# for form in forms:
#     number = form.text
#     pin = form.text
#     print(f'{number}  {pin}')