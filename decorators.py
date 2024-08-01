# decorators.py
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from config import FORCE_SUB_CHANNEL1, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3

def admin_required(func):
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        if user_id in [FORCE_SUB_CHANNEL1, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3]:
            await func(client, message)
        else:
            await message.reply("This command is only for admins.")
    return wrapper

def command_decorator(command_name):
    def decorator(func):
        async def wrapper(client: Client, message: Message):
            await func(client, message)
        return wrapper
    return decorator

def callback_decorator(callback_data):
    def decorator(func):
        async def wrapper(client: Client, callback_query: CallbackQuery):
            await func(client, callback_query)
        return wrapper
    return decorator
