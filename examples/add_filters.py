import asyncio
import zjson # pip3 install zjson

from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_helper import ApiException
from telebot.types import Message
from telemod import Listener, TimeOut

loop = asyncio.get_event_loop()
bot = AsyncTeleBot(token="")
listener = Listener(bot=bot, loop=loop)
db = zjson.AsyncClient("database.json", directory="cache")

async def check_admins(chat_id: int, user_id: int) -> bool:
    try:
        getChatMember = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    except ApiException:
        return False

    if getChatMember.status in {"administrator", "creator"}:
        return True
    else:
        return False

@bot.message_handler(content_types=["text"], chat_types=["supergroup"])
async def handler(message: Message):
    if message.text == "اضف رد":
        check = await check_admins(message.chat.id, message.from_user.id)
        if not check:
            return await bot.reply_to(message, "هذا الأمر يخص المشرفين فقط")
        else:
            try:
                rep_ = await listener.listen_to(
                    m=message,
                    text="ارسل كلمة الرد الان",
                    filters=["text"],
                    timeout=300 # المستخدم مايقدر يجاوب بعد 300 ثانية ( اختياري ) - للتقليل من استهلاك ال CPU
                )
                if (rep_.text == "الغاء"):
                    return await bot.reply_to(rep_, "تم الالغاء")
                rep__ = await listener.listen_to(
                    m=rep_,
                    text="ارسل جواب الرد الآن",
                    filters=["text"], # بامكانك اضافة جميع انواع الردود مو فقط نص ( هذا ملف تعليمي فقط )
                    timeout=300
                )
                if (rep__.text == "الغاء"):
                    return await bot.reply_to(rep_, "تم الالغاء")
                group_database = await db.get(f"{message.chat.id}") or {}
                group_database[rep_.text]={"type": "text", "rep": rep__.html_text}
                await db.set(f"{message.chat.id}", group_database)
                return await bot.reply_to(rep__, f"تم اضافة الرد ( {rep_.text} )")
            except TimeOut:
                return False

    elif message.text == "حذف رد":
        check = await check_admins(message.chat.id, message.from_user.id)
        if not check:
            return await bot.reply_to(message, "هذا الأمر يخص المشرفين فقط")
        else:
            try:
                rep_ = await listener.listen_to(
                    m=message,
                    text="ارسل كلمة الرد الان",
                    filters=["text"],
                    timeout=300
                )
                if (rep_.text == "الغاء"):
                    return await bot.reply_to(rep_, "تم الالغاء")
                group_database = await db.get(f"{message.chat.id}")
                if rep_.text not in group_database:
                    return await bot.reply_to(rep_, f"{rep_.text}\n- هذا الرد غير مضاف")
                else:
                    del group_database[rep_.text]
                    await db.set(f"{message.chat.id}", group_database)
                    return await bot.reply_to(rep_, f"{rep_.text}\n- تم مسح الرد بنجاح")
            except TimeOut:
                return False

    elif message.text == "الردود":
        check = await check_admins(message.chat.id, message.from_user.id)
        if not check:
            return await bot.reply_to(message, "هذا الأمر يخص المشرفين فقط")
        else:
            group_database = await db.get(f"{message.chat.id}")
            if not group_database:
                return await bot.reply_to(message, "لا يوجد ردود بالمجموعة")
            else:
                __ = "الردود:\n\n"
                count = 1
                for _ in group_database:
                    __ += f"{count} ) {_} - {group_database[_]['type']}\n";count+=1
                return await bot.reply_to(message, __)

    elif message.text == "تفعيل الردود":
        check = await check_admins(message.chat.id, message.from_user.id)
        if not check:
            return await bot.reply_to(message, "هذا الأمر يخص المشرفين فقط")
        else:
            if not await db.get(f"{message.chat.id}-disfilters"):
                return await bot.reply_to(message, "تم تفعيل الردود مسبقًا")
            else:
                await db.delete(f"{message.chat.id}-disfilters")
                return await bot.reply_to(message, "تم تفعيل الردود")

    elif message.text == "تعطيل الردود":
        check = await check_admins(message.chat.id, message.from_user.id)
        if not check:
            return await bot.reply_to(message, "هذا الأمر يخص المشرفين فقط")
        else:
            if await db.get(f"{message.chat.id}-disfilters"):
                return await bot.reply_to(message, "تم تعطيل الردود مسبقًا")
            else:
                await db.set(f"{message.chat.id}-disfilters", True)
                return await bot.reply_to(message, "تم تعطيل الردود")

    group_database = await db.get(f"{message.chat.id}")
    dis_filters = await db.get(f"{message.chat.id}-disfilters")
    if (group_database) and (message.text in group_database) and (not dis_filters):
            return await bot.reply_to(
            message,
            group_database[message.text]['rep'],
            parse_mode='html'
        )

async def main():
    print((await bot.get_me()).first_name)
    await bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    loop.run_until_complete(main())
