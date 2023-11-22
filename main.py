import os

from keyboards import keyboards_client

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from dotenv import load_dotenv

load_dotenv()

bot = Bot(os.getenv('BOT_TOKEN'))

dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот начал свою работу')


@dp.message_handler(commands=['start', 'help'])
async def help_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Описание возможностей бота',
        reply_markup=keyboards_client)


@dp.message_handler(commands=['add'])
async def help_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Добавить данные для проверки',
        reply_markup=keyboards_client)


@dp.message_handler(commands=['check'])
async def help_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Узнать статус проверки',
        reply_markup=keyboards_client)


@dp.message_handler(commands=['show'])
async def help_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Показать данные пользвователя',
        reply_markup=keyboards_client)


@dp.message_handler(commands=['delete'])
async def help_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Удалить данные из БД',
        reply_markup=keyboards_client)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
