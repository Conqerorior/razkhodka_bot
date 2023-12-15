import asyncio
import logging
import os
from typing import Any

import aioschedule
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from dotenv import load_dotenv

from keyboards import keyboards_client
from MongoData import (create_user, delete_user, get_all_users, get_user,
                       show_user, start_mongodb)
from parser_status import get_data_parser

load_dotenv()

storage = MemoryStorage()

bot = Bot(os.getenv('BOT_TOKEN'))

dp = Dispatcher(bot, storage=storage)


class AddUsers(StatesGroup):
    record_number = State()
    pin_number = State()


async def on_startup(_: Any) -> None:
    """
    Запуск бота.
    Инициализирует подключение к базе данных MongoDB,
    и запускает планировщик задач.
    """
    logging.warning('Бот начал свою работу')
    await start_mongodb()
    schedule_task = asyncio.create_task(scheduler())
    logging.warning(f'Запуск Планировщика {schedule_task.get_name()}')


async def scheduler_auto_status():
    """
    Обрабатывает запросы на получение статуса заявок.

    Получает список всех пользователей из базы данных,
    и для каждого пользователя отправляет ему сообщение
    с текущим статусом заявки.
    """
    users = await get_all_users()
    if users:
        for user in users:
            data = await get_data_parser(
                req_num=user['reqNum'], pin=user['pin'])

            await bot.send_message(user['user_id'],
                                   text=f'🇧🇬Добрый день, '
                                        f'*{user["username"]}*\\!\n'
                                        f'Статус заявки '
                                        f'под номером: {user["reqNum"]}'
                                        f'\n\n`{data["answer"].upper()}`\n\n'
                                        f'{data["time_answer"]}📅',
                                   parse_mode="MarkdownV2")

        return
    logging.warning('В Базе Данных нет пользователей')


async def scheduler():
    """
    Планировщик задач.

    Запускает функцию scheduler_auto_status
    ежедневно в 12:00.
    """
    aioschedule.every(1).days.at('12:00').do(scheduler_auto_status)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


@dp.message_handler(commands=['start', 'help'])
async def process_help_command(message: types.Message):
    """Обработка команды /start."""
    await bot.send_message(
        message.from_user.id,
        text='Описание возможностей бота',
        reply_markup=keyboards_client)


@dp.message_handler(commands=['add'], state=None)
async def process_add_command(message: types.Message):
    """
    Обработка команды /add.

    Проверяет, есть ли данные пользователя в базе данных,
    и если нет, то запускает машинное состояние (FSMContext)
    а так же, диалог добавления новой записи.

    :param message: Сообщение от пользователя.
    """
    instance = await get_user(message.from_user)
    if instance:
        await message.answer('Ваши данные уже внесены')
        return

    await AddUsers.record_number.set()
    await message.answer('Введите номер входящей заявки указывается '
                         'в формате «номер/год». Пример: «123/2016».\n'
                         '\nДля отмены введите /cancel')


@dp.message_handler(commands=['cancel'], state='*')
async def process_cancel(message: types.Message, state: FSMContext):
    """
    Обработка команды /cancel.

    В любом состоянии диалога.
    Завершает диалог и отправляет подтверждение.

    :param message: Сообщение от пользователя.
    :param state: Состояние диалога.
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


@dp.message_handler(lambda message: '/' not in message.text or not all(
    part.isdigit() for part in message.text.split('/')),
    state=AddUsers.record_number)
async def process_invalid_number(message: types.Message):
    """
    Обработка некорректно введенного номера заявки.
    Отправляет сообщение с примером правильного формата.

    :param message: Сообщение от пользователя.
    """
    await message.reply('Пример: «123/2016»')


@dp.message_handler(state=AddUsers.record_number)
async def process_add_number(message: types.Message, state: FSMContext):
    """
    Обработка введенного номера заявки.
    Сохраняет номер в данных диалога и переходит к следующему шагу.

    :param message: Сообщение от пользователя.
    :param state: Текущее состояние диалога.
    """
    async with state.proxy() as data:
        data['reqNum'] = message.text

    await AddUsers.next()
    await message.answer('ПИН-код вводится в документ, который вы получили'
                         ' при подаче заявления на стойке в Дирекции.\n'
                         '\nДля отмены введите /cancel')
    await AddUsers.pin_number.set()


@dp.message_handler(lambda message: not message.text.isdigit(),
                    state=AddUsers.pin_number)
async def process_invalid_pin(message: types.Message):
    """
    Обработка некорректно введенного ПИН-кода.
    Отправляет сообщение о необходимости ввести только цифры.

    :param message: Сообщение от пользователя.
    """
    await message.answer('Введите только цифры')


@dp.message_handler(state=AddUsers.pin_number)
async def process_add_pin(message: types.Message, state: FSMContext):
    """
    Обработка введенного ПИН-кода.
    Создает нового пользователя в базе данных, отправляет подтверждение
    и завершает диалог.

    :param message: Сообщение от пользователя.
    :param state: Текущее состояние диалога.
    """
    async with state.proxy() as data:
        data['pin'] = message.text

    await create_user(state, message.from_user)
    await message.answer('Данные получены')

    await state.finish()


@dp.message_handler(commands=['check'])
async def process_check_command(message: types.Message):
    """
    Обработка команды /check.
    Проверяет наличие данных пользователя в базе данных,
    и если они есть, то отправляет ему текущий статус заявки.

    :param message: Сообщение от пользователя.
    """
    user = await get_user(message.from_user)
    if not user:
        await bot.send_message(message.from_user.id,
                               text='Для получения данных '
                                    'пожалуйста введите данные')
        return

    data = await get_data_parser(req_num=user['reqNum'], pin=user['pin'])
    await bot.send_message(message.from_user.id,
                           text=f'🇧🇬Добрый день, *{user["username"]}*\\!\n'
                                f'Статус заявки под номером: {user["reqNum"]}'
                                f'\n\n`{data["answer"].upper()}`\n\n'
                                f'{data["time_answer"]}',
                           parse_mode="MarkdownV2")


@dp.message_handler(commands=['show'])
async def process_show_command(message: types.Message):
    """
    Обработка команды /show.
    Проверяет наличие данных пользователя в базе данных
    и выводит их в случае успешного поиска.

    :param message: Сообщение от пользователя.
    """
    user_data = await show_user(user=message.from_user)
    if user_data:
        user = user_data[0]
        await bot.send_message(message.from_user.id,
                               text=f'Ваш ID: {user["user_id"]}\n'
                                    f'Username: {user["username"]}\n'
                                    f'Номер Заявления: {user["reqNum"]}\n'
                                    f'Пин-Код: {user["pin"]}'
                               )

        return
    await bot.send_message(message.from_user.id,
                           text='Для получения данных зарегистрируйтесь')


@dp.message_handler(commands=['delete'])
async def process_delete_command(message: types.Message):
    """
    Обработка команды /delete.
    Удалит данные пользователя из базы данных.

    :param message: Сообщение от пользователя.
    """
    user = message.from_user
    user_data = await delete_user(user=user)
    if user_data.deleted_count == 1:
        await bot.send_message(message.from_user.id,
                               text=f'Пользователь '
                                    f'{user.username} успешно удален')

        return
    await bot.send_message(message.from_user.id,
                           text=f'Пользователь '
                                f'{user.username} не найден')


@dp.message_handler()
async def process_unknown_command(message: types.Message):
    """
    Обработка любых неизвестных команд.
    Отправляет пользователю сообщение с просьбой выбрать
    команду из списка и удалит сообщение.

    :param message: Сообщение от пользователя.
    """
    await message.answer('Выберите команду из списка')
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
