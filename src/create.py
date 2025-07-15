import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from DB.db import DataBase
from GLOBAL import API


bot = Bot(token=API, parse_mode=types.ParseMode.HTML)
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)
db = DataBase()