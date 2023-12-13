import logging

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
collection = client.razkhodka_db.razkhodka_users


async def start_mongodb():
    logging.warning('Запуск Базы Данных')


async def create_user(state, user):
    async with state.proxy() as data:
        load_data = {
            "user_id": user.id,
            "username": user.username,
            "reqNum": data['reqNum'],
            "pin": data['pin']
        }

    await collection.insert_one(load_data)


async def get_user(user):
    return await collection.find_one({"user_id": user.id})


async def show_user(user):
    cursor = collection.find({"user_id": user.id})
    user_data = []
    async for document in cursor:
        user_data.append(document)

    return user_data


async def delete_user(user):
    result = await collection.delete_one({'user_id': user.id})

    return result
