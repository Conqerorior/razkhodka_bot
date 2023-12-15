import datetime

import httpx
from bs4 import BeautifulSoup


async def get_data_parser(req_num, pin):
    async with httpx.AsyncClient() as client:
        headers = {
            'Accept': 'text/html',
            'User-Agent': 'Mozilla/5.0'
                          '(Windows NT 6.1)'
                          'AppleWebKit/537.36'
                          '(KHTML, like Gecko) '
                          'Chrome/29.0.1547.0 Safari/537.36'}

        response = await client.get(url='https://publicbg.mjs.bg/BgInfo/',
                                    headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')
        token = soup.find('form').find('input').get('value')

        data = {
            '__RequestVerificationToken': token,
            'reqNum': req_num,
            'pin': pin
        }

        result = await client.post(
            url='https://publicbg.mjs.bg/BgInfo/Home/Enroll',
            headers=headers,
            data=data)

        answer = BeautifulSoup(result.text, 'lxml')
        parser_answer = answer.find(
            name='div', class_='validation-summary-errors text-danger')
        today = datetime.datetime.today().strftime('%d\\.%m\\.%Y' + 'г\\.')

        data_answer = {
            'answer': parser_answer.text.strip(),
            'date_answer': today
        }

        return data_answer
