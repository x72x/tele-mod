from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

from config import listener

async def callback_query(query: CallbackQuery, bot: AsyncTeleBot):
    msg = await listener.listen_to(
        m=query,
        text="What's your name?",
        filters=["text"],
        reply_to_message_id=query.message.id
    )
    return await bot.reply_to(msg, f"Hi {msg.text}!")
