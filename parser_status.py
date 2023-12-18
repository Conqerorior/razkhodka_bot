import datetime
import logging

import httpx
from bs4 import BeautifulSoup

from message import message_status


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

        today = datetime.datetime.today().strftime(
            '%H:%M%n%d\\.%m\\.%Y' + 'г\\.')

        data_answer = {
            'answer': 'Ошибка обработки сервера',
            'time_answer': today
        }

        response = await client.get(url='https://publicbg.mjs.bg/BgInfo/',
                                    headers=headers)

        if response.status_code != 200:
            logging.critical(f'Ошибка в пути GET response:\n{response}')

            return data_answer

        try:
            soup = BeautifulSoup(response.text, 'lxml')
            token = soup.find('form').find('input').get('value')
        except AttributeError:
            logging.critical('Ошибка в получении ТОКЕНА')

            return data_answer

        data = {
            '__RequestVerificationToken': token,
            'reqNum': req_num,
            'pin': pin
        }

        result = await client.post(
            url='https://publicbg.mjs.bg/BgInfo/Home/Enroll',
            headers=headers,
            data=data)

        if result.status_code != 200:
            logging.critical(f'Ошибка при POST запросе result:\n{result}')

            return data_answer

        answer = BeautifulSoup(result.text, 'lxml')
        parser_answer = answer.find(
                name='div', class_='validation-summary-errors text-danger')

        if parser_answer is None:
            logging.critical('Ошибка при получении ответа parser_answer')

            return data_answer

        rus_answer = ''.join(parser_answer.text.strip().split('\n')[1:])

        parser_answer = parser_answer.text.strip()

        status = rus_answer if rus_answer else parser_answer

        data_answer = {
            'answer': message_status.get(status, status),
            'time_answer': today
        }

        return data_answer
