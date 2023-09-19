import asyncio
from telebot.async_telebot import AsyncTeleBot
from telemod import Listener

loop = asyncio.get_event_loop()
bot = AsyncTeleBot(token="")
listener = Listener(bot=bot, loop=loop)
