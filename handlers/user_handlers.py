from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ContentType
from lexicon.lexicon import MESSAGES
from database.users_sqlite import load_users_config, save_users_config
from database.stats_data import save_stats
from services.services import translate, hash_user_id
from keyboards.keyboards import create_language_keyboard
from config_data.langs import bot_lang_from, bot_lang_to, reversed_bot_lang_from, reversed_bot_lang_to

router = Router()
users_config = load_users_config()


async def get_user_data(message: Message) -> tuple:
    user_id = str(message.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    return hashed_user_id, reversed_bot_lang_from.get(
        users_config[hashed_user_id]['src_lang']), reversed_bot_lang_to.get(users_config[hashed_user_id]['dest_lang'])


@router.message(Command(commands='start'))
async def start(message: Message):
    hashed_user_id, _, _ = await get_user_data(message)
    if hashed_user_id not in users_config:
        users_config[hashed_user_id] = {
            'src_lang': 'auto',
            'dest_lang': 'en'
        }
    src_name = reversed_bot_lang_from.get(users_config[hashed_user_id]['src_lang'])
    dest_name = reversed_bot_lang_to.get(users_config[hashed_user_id]['dest_lang'])
    save_users_config(users_config)
    await message.answer(MESSAGES['/start'] + f'\n{src_name} ->> '
                                              f'{dest_name}')


@router.message(Command(commands='change_language'))
async def change_language(message: Message):
    hashed_user_id, src_name, dest_name = await get_user_data(message)
    await message.answer(MESSAGES['/change_language'])
    await message.answer(f'Source: {src_name}', reply_markup=create_language_keyboard(bot_lang_from, prefix='FROM'))
    await message.answer(f'Destination: {dest_name}', reply_markup=create_language_keyboard(bot_lang_to, prefix='TO'))


@router.message(Command(commands='help'))
async def help(message: Message):
    await message.answer(MESSAGES['/help'])


@router.message(Command(commands='configs'))
async def help(message: Message):
    hashed_user_id, src_name, dest_name = await get_user_data(message)
    await message.answer(MESSAGES['/configs'] + f'\n{src_name} ->> '
                                                f'{dest_name}')


@router.message(F.content_type == ContentType.TEXT)
async def send_translation(message: Message):
    user_id = str(message.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    config_lang = (users_config[hashed_user_id][key] for key in ['src_lang', 'dest_lang'])
    translated_text = translate(message.text, src_lang=next(config_lang), dest_lang=next(config_lang))
    save_stats(users_config)
    await message.answer(translated_text)


@router.callback_query(F.data.startswith('FROM'))
async def source_lang(callback: CallbackQuery):
    language_code = callback.data.split('_')[-1]
    user_id = str(callback.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    users_config[hashed_user_id]['src_lang'] = language_code
    language_name = next((lang for lang, code in bot_lang_from.items() if code == language_code))
    save_users_config(users_config)
    await callback.message.edit_text(f'Source: {language_name}',
                                     reply_markup=create_language_keyboard(bot_lang_from, prefix='FROM'))


@router.callback_query(F.data.startswith('TO'))
async def destination_lang(callback: CallbackQuery):
    language_code = callback.data.split('_')[-1]
    user_id = str(callback.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    users_config[hashed_user_id]['dest_lang'] = language_code
    language_name = next((lang for lang, code in bot_lang_from.items() if code == language_code), None)
    save_users_config(users_config)
    await callback.message.edit_text(f'Destination: {language_name}',
                                     reply_markup=create_language_keyboard(bot_lang_to, prefix='TO'))
