import datetime

from bs4 import BeautifulSoup
from requests import Session


work = Session()

headers = {
    'User-Agent': 'Mozilla/5.0'
                  '(Windows NT 6.1)'
                  'AppleWebKit/537.36'
                  '(KHTML, like Gecko) '
                  'Chrome/29.0.1547.0 Safari/537.36'}

response = work.get(
    url='https://publicbg.mjs.bg/BgInfo/',
    headers=headers)

soup = BeautifulSoup(response.text, 'lxml')

token = soup.find('form').find('input').get('value')

data = {
    '__RequestVerificationToken': token,
    'reqNum': '1352/2023',
    'pin': '081209'
}

result = work.post(
    url='https://publicbg.mjs.bg/BgInfo/Home/Enroll',
    headers=headers,
    data=data)
answer = BeautifulSoup(result.text, 'lxml')

res = answer.find(
    name='div',
    class_='validation-summary-errors text-danger'
)
today = datetime.date.today().strftime("%d.%m.%Y" + 'г.')
print(today, res.text.strip(), sep='\n')
print('test')