from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

keyboard_help = KeyboardButton('/help')
keyboard_add = KeyboardButton('/add')
keyboard_check = KeyboardButton('/check')
keyboard_show = KeyboardButton('/show')
keyboard_delete = KeyboardButton('/delete')

keyboards_client = ReplyKeyboardMarkup(resize_keyboard=True)

(keyboards_client.add(keyboard_help).row(keyboard_add, keyboard_check).row(
    keyboard_show, keyboard_delete))
