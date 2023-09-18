from telebot import async_telebot, types
from telemod import Listener
import asyncio

bot = async_telebot.AsyncTeleBot(token="")
loop = asyncio.get_event_loop()
listener = Listener(bot=bot, loop=loop)

@bot.message_handler(commands=["start"])
async def _(message: types.Message):
    msg = await listener.listen_to(message, "Send a photo", filters=["photo"])
    return await bot.reply_to(msg, msg.photo[0].file_id)

async def main():
    print((await bot.get_me()).first_name)
    # await listener.start()
    await bot.infinity_polling()

loop.run_until_complete(main())
