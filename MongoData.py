import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
collection = client.razkhodka_db.razkhodka_users


async def create_user(user):
    await collection.insert_one(user)


async def get_user(user):
    await collection.find_one(user)

# collection.insert_one(pattern)
