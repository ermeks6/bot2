from config import dp, bot, ADMINS
import logging
from aiogram import types
from aiogram.utils import executor
from aiogram.types import ParseMode
from datetime import datetime, timedelta
import asyncio


logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот для напоминания о задачах. Отправь мне сообщение в формате: /add_task Название задачи | Дата и время напоминания (гггг-мм-дд чч:мм:сс)")


@dp.message_handler(commands=['add_task'])
async def add_task(message: types.Message):
    try:
        text = message.text.split('|')
        task = text[0].replace('/add_task', '').strip()
        task_date = datetime.strptime(text[1].strip(), '%Y-%m-%d %H:%M:%S')

        await message.reply(f'Задача "{task}" успешно добавлена! Я напомню вам о ней {task_date}')

        delta = task_date - datetime.now()
        await asyncio.sleep(delta.total_seconds())
        await bot.send_message(message.chat.id, f'Напоминаю о задаче "{task}"!', parse_mode=ParseMode.HTML)

    except Exception as e:
        logging.exception(e)
        await message.reply('Произошла ошибка при создании задачи. Проверьте формат введенных данных и попробуйте снова.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

