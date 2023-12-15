import logging
import os
from typing import Any, Optional

import motor.motor_asyncio
from pymongo.results import DeleteResult

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB'))
collection = client.razkhodka_db.razkhodka_users


async def start_mongodb():
    logging.warning('Запуск Базы Данных')


async def create_user(state: Any, user: Any) -> None:
    """Создает нового пользователя в базе данных."""
    async with state.proxy() as data:
        load_data = {
            "user_id": user.id,
            "username": user.username,
            "reqNum": data['reqNum'],
            "pin": data['pin']
        }

    await collection.insert_one(load_data)


async def get_user(user: Any) -> dict:
    """Получает данные о пользователе из базы данных."""
    return await collection.find_one({"user_id": user.id})


async def get_all_users() -> list[dict[str, Any]]:
    """Получает список всех пользователей из базы данных."""
    cursor = collection.find()
    all_users = await cursor.to_list(length=None)
    return all_users


async def show_user(user: Any) -> Optional[list[dict[str, Any]]]:
    """Возвращает список информации о пользователе из базы данных."""
    cursor = collection.find({"user_id": user.id})
    user_data = []
    async for document in cursor:
        user_data.append(document)

    return user_data


async def delete_user(user: Any) -> Optional[DeleteResult]:
    """Удаляет пользователя из базы данных."""
    result = await collection.delete_one({'user_id': user.id})

    return result
