import logging
import os

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from dotenv import load_dotenv

from keyboards import keyboards_client
from MongoData import create_user, get_user, start_mongodb, show_user, \
    delete_user

load_dotenv()

storage = MemoryStorage()

bot = Bot(os.getenv('BOT_TOKEN'))

dp = Dispatcher(bot, storage=storage)


class AddUsers(StatesGroup):
    record_number = State()
    pin_number = State()


async def on_startup(_):
    logging.warning('Бот начал свою работу')
    await start_mongodb()


@dp.message_handler(commands=['start', 'help'])
async def process_help_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Описание возможностей бота',
        reply_markup=keyboards_client)


@dp.message_handler(commands=['add'], state=None)
async def process_add_command(message: types.Message):
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
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


@dp.message_handler(lambda message: '/' not in message.text or not all(
    part.isdigit() for part in message.text.split('/')),
                    state=AddUsers.record_number)
async def process_invalid_number(message: types.Message):
    await message.reply('Пример: «123/2016»')


@dp.message_handler(state=AddUsers.record_number)
async def process_add_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(data)
        data['reqNum'] = message.text

    await AddUsers.next()
    await message.answer('ПИН-код вводится в документ, который вы получили'
                         ' при подаче заявления на стойке в Дирекции.\n'
                         '\nДля отмены введите /cancel')
    await AddUsers.pin_number.set()


@dp.message_handler(lambda message: not message.text.isdigit(),
                    state=AddUsers.pin_number)
async def process_invalid_pin(message: types.Message):
    await message.answer('Введите только цифры')


@dp.message_handler(state=AddUsers.pin_number)
async def process_add_pin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(data)
        data['pin'] = message.text

    await create_user(state, message.from_user)
    await message.answer('Данные получены')

    await state.finish()


@dp.message_handler(commands=['check'])
async def process_check_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Узнать статус проверки',
        reply_markup=keyboards_client)


@dp.message_handler(commands=['show'])
async def process_show_command(message: types.Message):
    user_data = await show_user(user=message.from_user)
    await bot.send_message(message.from_user.id, user_data)


@dp.message_handler(commands=['delete'])
async def process_delete_command(message: types.Message):
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
    await message.answer('Выберите команду из списка')
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
