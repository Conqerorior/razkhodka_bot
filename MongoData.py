import logging
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
collection = client.razkhodka_db.razkhodka_users


async def start_mongodb():
    logging.warning('Запуск Базы Данных')


async def create_user(state, user):
    async with state.proxy() as data:
        data_value = list(data)
        load_data = {
            "user_id": user.id,
            "username": user.username,
            "reqNum": data_value[0],
            "pin": data_value[1]
        }

    await collection.insert_one(load_data)


async def get_user(user):
    return await collection.find_one({"user_id": user.id})
