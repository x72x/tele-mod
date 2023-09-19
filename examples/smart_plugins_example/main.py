from config import bot, loop
from handlers import start_handler, callback_query

bot.register_callback_query_handler(callback_query, func= lambda query: query.data == "1", pass_bot=True)
bot.register_message_handler(start_handler, commands=["start"], pass_bot=True)

async def main():
    print((await bot.get_me()).full_name)
    await bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    loop.run_until_complete(main())
