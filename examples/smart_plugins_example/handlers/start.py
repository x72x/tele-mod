from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import listener

async def start_handler(message: Message, bot: AsyncTeleBot):
    msg = await listener.listen_to(
        m=message,
        text="What's your name?",
        filters=["text"],
        reply_to_message_id=message.id
    )
    buttons = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Try callback query", callback_data="1")
    )
    return await bot.reply_to(msg, f"Your name is {msg.text}", reply_markup=buttons)
