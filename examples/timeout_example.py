import asyncio
from telebot import async_telebot, types
from telemod import Listener, TimeOut

bot = async_telebot.AsyncTeleBot(token="")
loop = asyncio.get_event_loop()

listener = Listener(bot=bot, loop=loop)

@bot.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    try:
        msg = await listener.listen_to(message, "What's your name?", timeout=10)
    except TimeOut:
        msg = None
        await bot.reply_to(message, "Time Out")
    if msg:
        return await bot.reply_to(msg, f"Hi {msg.text}")

async def main():
    print((await bot.get_me()).first_name)
    # await listener.start()
    await bot.infinity_polling(skip_pending=True)

loop.run_until_complete(main())
