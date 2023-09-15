import asyncio
import json
from time import sleep
from typing import List, Union
from datetime import datetime, timedelta

from telebot import types, async_telebot
from telebot.handler_backends import ContinueHandling

class TimeOut(Exception):
    pass

class botAlreadyConnected(Exception):
    pass

_cache = {}

available_filters = [
    "text", "document", "animation", "sticker", "photo", "video",
    "contact", "location", "voice", "video_note", "venue", "dice",
    "poll", "audio"
]

class Listener:
    def __init__(self, bot: async_telebot.AsyncTeleBot, loop: asyncio.AbstractEventLoop, show_output: bool = True) -> None:
        super().__init__()
        bot_id = bot.token.split(":")[0]
        if bot_id in _cache:
            raise botAlreadyConnected(f"Client [ {bot_id} ] Already connected")

        self.loop = loop
        _cache[bot_id]={}
        _cache[bot_id]['list']=[]
        self.bot = bot
        self.name = bot_id
        self.show_output = show_output

    async def start(self):
        def __():
            self.bot.register_message_handler(self._handler)
        self.loop.run_in_executor(None, __)

    async def listen(
        self,
        chat_id: int,
        text: str = None,
        from_id: Union[List[int], int] = None,
        protect_content: bool = None,
        reply_to_message_id: int = None,
        filters: List[str] = available_filters,
        disable_web_page_preview: bool = True,
        timeout: int = None,
        parse_mode=None,
        reply_markup=None,
        *args,
        **kwargs
    ) -> types.Message:
        """
        Args:
            chat_id (int): Chat ID
            from_id (List[int], int, optional): Only listening from specific ids or id ( User ID or Chat ID ). Defaults to None.
            text (str): The question.
            protect_content (bool, optional): Protect message content. Defaults to None.
            reply_to_message_id (int, optional): message to reply. Defaults to None.
            content_filters (List[str], optional): List of filters like: ['text', 'photo'] ( Message type attributes ). Defaults to None.
            disable_web_page_preview (bool, optional): Defaults to True.
            parse_mode (str, optional): Defaults to None.
            reply_markup (optional): Defaults to None.
            *args, **kwargs

        Returns:
            telebot.types.Message: Message type, with 'output' attribute when you set show_output as True
        """
        data = {
                "from_id": from_id,
                "filters": filters,
                "chat_id": chat_id,
        }
        if data in _cache[self.name]['list']: _cache[self.name]['list'].remove(data)
        _cache[self.name]['list'].append(data)
        if text:
            m = await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
                reply_to_message_id=reply_to_message_id,
                disable_web_page_preview=disable_web_page_preview,
                protect_content=protect_content,
                parse_mode=parse_mode,
                *args,
                **kwargs
            )
        else:
            m = None
        _cache[self.name][json.dumps(data, ensure_ascii=False)]=m
        if timeout:
            stamp = (datetime.now() + timedelta(seconds=timeout))
        def ___():
            while data in _cache[self.name]['list']:
                if timeout:
                    if datetime.now() > stamp:
                        raise TimeOut("Time out error")
                sleep(0)
            return _cache[self.name][json.dumps(data, ensure_ascii=False)]
        return await self.loop.run_in_executor(None, ___)

    async def listen_to(self, m: Union[types.CallbackQuery, types.Message], text : str, *args, **kwargs):
        if isinstance(m, types.CallbackQuery):
            chat_id = m.message.chat.id
            from_id = m.from_user.id
            reply_to_message_id = None
        elif isinstance(m, types.Message):
            chat_id = m.chat.id
            from_id = (m.from_user or m.sender_chat).id
            reply_to_message_id = m.id
        return await self.listen(chat_id=chat_id, from_id=from_id, text=text, reply_to_message_id=reply_to_message_id, *args, **kwargs)

    async def _handler(self, message: types.Message):
            sender = message.sender_chat or message.from_user
            chat_id = message.chat.id
            __ = []
            for data in _cache[self.name]['list']:
                if (data['chat_id'] == chat_id) and (
                    (data["from_id"] is None) or (isinstance(data["from_id"], list) and sender.id in data["from_id"]) or (
                        isinstance(data["from_id"], int) and data["from_id"] == sender.id
                    )
                ):
                    for _ in data["filters"]:
                        if __: break
                        if hasattr(message, _) and getattr(message, _):
                            __.append(_)
                    if not __:
                        return False
                    if self.show_output:
                        message.output = _cache[self.name][json.dumps(data, ensure_ascii=False)]
                    _cache[self.name][json.dumps(data, ensure_ascii=False)]=message
                    _cache[self.name]['list'].remove(data)
            return ContinueHandling()
