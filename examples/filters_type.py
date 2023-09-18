from telebot import async_telebot, types
from telemod import Listener
import asyncio

bot = async_telebot.AsyncTeleBot(token="")
loop = asyncio.get_event_loop()
listener = Listener(bot=bot, loop=loop)

@bot.message_handler(commands=["ask"], chat_types=["supergroup"])
async def _(message: types.Message):
    msg = await listener.listen(
        chat_id=message.chat.id,
        text="What's your name",
        filters=["sender_chat", "text"],
        filters_type=2
    ) # will only listen to an message has "sender_chat" and "text" attribute
    msg = await listener.listen(
        chat_id=message.chat.id,
        text="What's your name",
        filters=["sender_chat", "text"],
        filters_type=1
    ) # will listen to any messgae has "sender_chat" or "text" attribute
    return await bot.reply_to(msg, msg.text)

async def main():
    print((await bot.get_me()).first_name)
    # await listener.start()
    await bot.infinity_polling()

loop.run_until_complete(main())
