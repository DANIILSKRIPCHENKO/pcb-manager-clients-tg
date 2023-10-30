from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram import flags
from aiogram.fsm.context import FSMContext
from states import Gen
from aiogram import Bot
from services.image_processor_service import ImageProcessorService
import uuid
import json

import text as txt
import menu as mn

router = Router()
image_processor_service = ImageProcessorService()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(txt.greet.format(name=message.from_user.full_name), reply_markup=mn.menu)

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(txt.menu, reply_markup=mn.menu)

@router.callback_query(F.data == "generate_json")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.json_prompt)
    await clbck.message.edit_text(txt.gen_text)
    await clbck.message.answer(txt.gen_exit, reply_markup=mn.exit_kb)

@router.message(Gen.json_prompt)
@flags.chat_action(initial_sleep=2, action="upload_document", interval=3)
async def echo_handler(message: Message, bot: Bot) -> None:
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    loadedFile = await bot.download_file(file.file_path)
    defect_details = await image_processor_service.get_defect_details(loadedFile)
    json_bytes = json.dumps(defect_details).encode('utf-8')
    document = types.BufferedInputFile(json_bytes, str(uuid.uuid4()) + ".json")
    await bot.send_document(chat_id=message.chat.id, document=document)
        

@router.callback_query(F.data == "generate_image")
async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.image_prompt)
    await clbck.message.edit_text(txt.gen_image)
    await clbck.message.answer(txt.gen_exit, reply_markup=mn.exit_kb)

@router.message(Gen.image_prompt)
@flags.chat_action(initial_sleep=2, action="upload_document", interval=3)
async def generate_image(message: Message, bot: Bot):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    loadedFile = await bot.download_file(file.file_path)
    defect_file_bytes = await image_processor_service.get_defect_file(loadedFile)
    document = types.BufferedInputFile(defect_file_bytes, str(uuid.uuid4()) + ".jpg")
    await bot.send_document(chat_id=message.chat.id, document=document)

