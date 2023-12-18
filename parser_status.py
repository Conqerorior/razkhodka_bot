import datetime
import logging

import httpx
from bs4 import BeautifulSoup


async def get_data_parser(req_num: str, pin: str) -> dict[str, str]:
    """
    Асинхронная функция для получения статуса заявления из официального сайта.

    Вход:
        req_num: Входящий номер заявки
        pin: ПИН-код

    Выход:
        data_answer: Словарь с ответом статуса заявления
    """

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
        if response.status_code != 200:
            logging.critical(f'Ошибка в пути GET response:\n{response}')
            data_answer = {
                'answer': 'Ошибка обработки сервера',
                'time_answer': datetime.datetime.today().strftime(
                    '%H:%M%n%d\\.%m\\.%Y' + 'г\\.')
            }

            return data_answer

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
        today = datetime.datetime.today().strftime(
            '%H:%M%n%d\\.%m\\.%Y' + 'г\\.')

        data_answer = {
            'answer': parser_answer.text.strip(),
            'time_answer': today
        }

        return data_answer
