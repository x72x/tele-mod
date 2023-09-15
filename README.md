## Installing
```bash
pip3 install -U telemod
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
    await listener.start()
    await bot.infinity_polling(skip_pending=True)

loop.run_until_complete(main())
```

## Community
- Join To Our Channel: https://t.me/Y88F8
