## Installing
```bash
pip3 install -U tele-mod
```

## Telemod
> Message listener example

```python
import asyncio
from telebot import async_telebot, types
from telemod import Listener

bot = async_telebot.AsyncTeleBot(token="")
loop = asyncio.get_event_loop()

listener = Listener(bot=bot, loop=loop)

@bot.message_handler(commands=["start"])
async def _(message: types.Message):
    msg = await listener.listen_to(m=message, text="What's Your name?")
    await bot.reply_to(msg, f"Your name is {msg.text}")
    # to delete question message
    # await bot.delete_message(chat_id=message.chat.id, message_id=msg.output.id)

async def main():
    print((await bot.get_me()).first_name)
    await bot.infinity_polling(skip_pending=True)

loop.run_until_complete(main())
```

> CallbackQuery Listener Example

```python
@bot.callback_query_handler(func = lambda query: True)
async def _(query: types.CallbackQuery):
    if query.data == "name":
        msg = await listener.listen_to(
            query,
            "What's your name?",
            filters=["text"]
        )
        return await bot.reply_to(msg, f"Your name is {msg.text}")
```

> Simple usage example

```python
msg = await listener.listen(
    chat_id=chat_id,
    text="What's your name",
    from_id=from_id,
    filters=["text", "photo"]
)
print(msg)
```

> Time out example

```python
@bot.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    try:
        msg = await listener.listen_to(message, "What's your name?", timeout=10)
    except TimeOut:
        msg = None
        await bot.reply_to(message, "Time Out")
    if msg:
        return await bot.reply_to(msg, f"Hi {msg.text}")
```

> Filters type example

```python
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
```

## Community
- Join To Our Channel: https://t.me/Y88F8
