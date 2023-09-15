import asyncio
from telebot import async_telebot, types
from telemod import Listener

bot = async_telebot.AsyncTeleBot(token="")
loop = asyncio.get_event_loop()

listener = Listener(bot=bot, loop=loop)

@bot.message_handler(content_types=["photo"])
async def start_handler(message: types.Message):
    await bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.id,
        reply_to_message_id=message.id,
        caption="Send y/n to add buttons to this photo"
    )
    # wait to message without send question
    msg = await listener.listen(
        message.chat.id,
        from_id=(message.from_user or message.sender_chat).id,
        filters=['text']
    )
    if msg.text.lower() == "y":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("1", callback_data="1"), types.InlineKeyboardButton("2", callback_data="2")
        )
        return await bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=message.chat.id,
            message_id=message.id,
            reply_to_message_id=msg.id,
            reply_markup=markup
        )
    elif msg.text.lower() == "n":
        return await bot.reply_to(msg, "Okay")
    else:
        return await bot.reply_to(msg, "Wrong choice")


async def main():
    print((await bot.get_me()).first_name)
    await listener.start()
    await bot.infinity_polling(skip_pending=True)

loop.run_until_complete(main())
