import Config

import asyncio
import logging
import datetime

from aiogram import Dispatcher, types, Router, Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from Handlers import router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import MySQLdb
connect = MySQLdb.connect(user='USERNAME', password='PASSWORD', host='localhost', database='DATABASE')
cursor=connect.cursor()

class ReminderSet(StatesGroup):
    choosing_name = State()
    choosing_date = State()
    choosing_time = State()
    choosing_description = State()



router=Router()
#сообщение при старте
@router.message(Command("start"))
async def start_handler(msg: types.Message):
    await msg.answer("Привет! Я бот-напоминалка. Я умею запоминать события и сообщать о них.")

#ID
@router.message(Command("id"))
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")

#установка напоминания
@router.message(StateFilter(None), Command("remindset"))
async def ask_name(msg: Message, state: FSMContext):
    await msg.answer("Введите название события:")
    await state.set_state(ReminderSet.choosing_name)

@router.message(ReminderSet.choosing_name)
async def set_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text.lower())
    await msg.answer("Введите дату напоминания:")
    await state.set_state(ReminderSet.choosing_date)

@router.message(ReminderSet.choosing_date)
async def set_date(msg: Message, state: FSMContext):
    await state.update_data(date=msg.text.lower())
    await msg.answer("Введите время события:")
    await state.set_state(ReminderSet.choosing_time)

@router.message(ReminderSet.choosing_time)
async def set_time(msg: Message, state: FSMContext):
    await state.update_data(time=msg.text.lower())
    await msg.answer("Введите краткое описание события:")
    await state.set_state(ReminderSet.choosing_description)

@router.message(ReminderSet.choosing_description)
async def set_description(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text.lower())
    #await msg.answer("отправляю данные")
    userdata = await state.get_data()
    print(userdata['name'], userdata['description'], userdata['date'], userdata['time'])
    cursor.execute(
        """INSERT INTO reminders (user, name, date, time, description)
        VALUES (%s, %s, %s, %s, %s)""",
        (msg.from_user.id, userdata['name'], userdata['date'], userdata['time'], userdata['description'],))
    connect.commit()
    await state.clear()
    cursor.close()
    connect.close()


#бот
async def main():
    bot = Bot(token=Config.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())

