import asyncio
from telebot import async_telebot, types
from telemod import Listener

bot = async_telebot.AsyncTeleBot(token="")
loop = asyncio.get_event_loop()

listener = Listener(bot=bot, loop=loop)

@bot.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Name", callback_data="name"),
        types.InlineKeyboardButton("Age", callback_data="age")
    )
    return await bot.reply_to(message=message, text="Choose", reply_markup=markup)

@bot.callback_query_handler(func = lambda query: True)
async def callback_query(query: types.CallbackQuery):
    if query.data == "name":
        msg = await listener.listen_to(
            query,
            "What's your name?",
            filters=["text"]
        )
        return await bot.reply_to(msg, f"Your name is {msg.text}")
    elif query.data == "age":
        msg = await listener.listen_to(
            query,
            "How old are you?",
            filters=["text"]
        )
        return await bot.reply_to(msg, f"Your age is {msg.text}")

async def main():
    print((await bot.get_me()).first_name)
    # await listener.start()
    await bot.infinity_polling(skip_pending=True)

loop.run_until_complete(main())
