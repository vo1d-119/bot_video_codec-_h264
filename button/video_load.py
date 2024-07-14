import os
import time
import asyncio 
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
from main import bot

class Video_file(StatesGroup):
    arg = State()
 
async def convert_video(input_path, output_path):
    process = await asyncio.create_subprocess_exec(*["ffmpeg/ffmpeg.exe","-i", input_path, "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-c:a", "aac", "-strict", "experimental", output_path], stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        print(stderr.decode())
    else:
        print(output_path)

def setup(dp: Dispatcher):
    @dp.callback_query(lambda callback_query: callback_query.data == "load_video")
    async def video_loader(callback_query: types.CallbackQuery, state: FSMContext):
        await bot.send_message(chat_id=callback_query.message.chat.id, text="Загрузите видео: ") 
        await state.set_state(Video_file.arg)

    @dp.message(Video_file.arg)
    async def handle_video_file(message: types.Message, state: FSMContext):
        video =  message.document if not message.video else message.video
        await message.reply(f"Инфо: {video} ожидайте видео")
        await state.clear()
        file = await bot.get_file(video.file_id)
        original_video_file_path = os.path.join('videos', f"video_{message.from_user.id}_{video.file_unique_id}_{time.time()}{os.path.splitext(video.file_name)[1]}")    
        await bot.download_file(file.file_path, original_video_file_path)
        converted_video_file_path = os.path.join('videos_h264', os.path.basename(f"converted_video_{message.from_user.id}_{video.file_unique_id}_{time.time()}.mp4"))
        await convert_video(original_video_file_path, converted_video_file_path)
        await bot.send_video(chat_id=message.chat.id,video=FSInputFile(converted_video_file_path),reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Загрузить видео", callback_data="load_video")]]))
        os.remove(original_video_file_path)
        os.remove(converted_video_file_path)
    
    @dp.message()
    async def msg_heade(message: types.Message):
        message.document if not message.video else message.video