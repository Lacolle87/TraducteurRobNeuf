from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ContentType
from lexicon.lexicon import MESSAGES
from database.users_sqlite import load_users_config, save_users_config
from services.services import translate
from keyboards.keyboards import create_language_keyboard
from config_data.langs import bot_lang_from, bot_lang_to

router = Router()
users_config = load_users_config()


@router.message(Command(commands='start'))
async def start(message: Message):
    user_id = str(message.from_user.id)
    if user_id not in users_config:
        users_config[user_id] = {
            'src_lang': 'auto',
            'dest_lang': 'en'
        }
    src_name = next((lang for lang, code in bot_lang_from.items() if code == users_config[user_id]['src_lang']))
    dest_name = next((lang for lang, code in bot_lang_to.items() if code == users_config[user_id]['dest_lang']))
    save_users_config(users_config)
    await message.answer(MESSAGES['/start'] + f'\n{src_name} ->> '
                                              f'{dest_name}')


@router.message(Command(commands='change_language'))
async def start(message: Message):
    await message.answer('From:', reply_markup=create_language_keyboard(bot_lang_from, prefix='FROM'))
    await message.answer('To:', reply_markup=create_language_keyboard(bot_lang_to, prefix='TO'))


@router.message(Command(commands='help'))
async def help(message: Message):
    await message.answer(MESSAGES['/help'])


@router.message(F.content_type == ContentType.TEXT)
async def send_translation(message: Message):
    user_id = str(message.from_user.id)
    src_lang = users_config[user_id]['src_lang']
    dest_lang = users_config[user_id]['dest_lang']
    translated_text = translate(message.text, src_lang=src_lang, dest_lang=dest_lang)
    await message.answer(translated_text)


@router.callback_query(F.data.startswith('FROM'))
async def source_lang(callback: CallbackQuery):
    language_code = callback.data.split('_')[-1]
    user_id = str(callback.from_user.id)
    users_config[user_id]['src_lang'] = language_code
    language_name = next((lang for lang, code in bot_lang_from.items() if code == language_code))
    save_users_config(users_config)
    await callback.message.answer(f'Source: {language_name}')


@router.callback_query(F.data.startswith('TO'))
async def destination_lang(callback: CallbackQuery):
    language_code = callback.data.split('_')[-1]
    user_id = str(callback.from_user.id)
    users_config[user_id]['dest_lang'] = language_code
    language_name = next((lang for lang, code in bot_lang_from.items() if code == language_code), None)
    save_users_config(users_config)
    await callback.message.answer(f'Destination: {language_name}')
