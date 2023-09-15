import asyncio
from telebot import async_telebot, types
from telemod import Listener

bot = async_telebot.AsyncTeleBot(token="")
loop = asyncio.get_event_loop()

listener = Listener(bot=bot, loop=loop)

@bot.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    msg = await listener.listen_to(message, "What's your name?")
    msg2 = await listener.listen_to(msg, "how old are you?")
    return await bot.reply_to(
        msg2,
        f"Your name is {msg.text}\nAnd you're {msg2.text} year old"
    )

async def main():
    print((await bot.get_me()).first_name)
    await listener.start()
    await bot.infinity_polling(skip_pending=True)

loop.run_until_complete(main())
