import asyncio
import logging
from aiogram import Dispatcher, types, Router, Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import Config
from aiogram.filters import Command
import datetime

router=Router()

async def main():
    bot = Bot(token=Config.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
#start
@router.message(Command("start"))
async def start_handler(msg: types.Message):
    await msg.answer("Привет! Я бот-напоминалка. Я умею запоминать события и сообщать о них.")

#установка  напоминания
@router.message(Command("remind_set"))
async def reminder_name(msg: types.Message):
    await msg.answer("Назовите событие")
    await msg.answer(msg.text)
@router.message()
async def set_event(msg: types.Message):
    user_data = {}
    user_data[msg.chat.id] = {'reminder_name': msg.text}
    await msg.answer("Введите дату и время, когда вы хотите получить напоминание в формате ДД-ММ-ГГГГ чч:мм:сс.")
@router.message()
async def set_date(msg: types.Message):
    reminder_time = datetime.datetime.strptime(msg.text, '%d-%m-%Y %H:%M:%S')
    now = datetime.datetime.now()
    delta = reminder_time - now