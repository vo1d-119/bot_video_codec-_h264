from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Dispatcher
from aiogram.filters.command import Command

def setup(dp: Dispatcher):
    @dp.message(Command('start'))
    async def start_command(message: types.Message):
        await message.reply(text="Выбор действий", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Загрузить видео", callback_data="load_video")]]))