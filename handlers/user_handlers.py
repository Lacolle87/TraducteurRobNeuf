import logging
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ContentType, BufferedInputFile
from lexicon.lexicon import MESSAGES
from database.users_postgres import load_users_config, save_users_config
from database.users_stats import save_stats
from database.select_data import get_stats, stats_to_csv, generate_filename
from services.services import translate, hash_user_id
from keyboards.keyboards import create_language_keyboard
from config_data.langs import bot_lang_from, bot_lang_to, reversed_bot_lang_from, reversed_bot_lang_to
from config_data.config import load_config

config = load_config()
router = Router()


def get_hashed_user_id(message: Message) -> str:
    user_id = str(message.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    return hashed_user_id


def get_language_names(users_config: dict, hashed_user_id: str) -> tuple[str, str, str, str]:
    src_lang = users_config[hashed_user_id]['src_lang']
    dest_lang = users_config[hashed_user_id]['dest_lang']
    src_name = reversed_bot_lang_from.get(src_lang)
    dest_name = reversed_bot_lang_to.get(dest_lang)
    return src_name, dest_name, src_lang, dest_lang


@router.message(Command(commands='start'))
async def start_message(message: Message):
    user_id = str(message.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    users_config = load_users_config()
    if hashed_user_id not in users_config:
        users_config[hashed_user_id] = {
            'src_lang': 'auto',
            'dest_lang': 'en'
        }
        save_users_config(users_config)
        logging.info(f"New user {hashed_user_id[:8]} added to the configuration.")
    else:
        logging.info(f"User {hashed_user_id[:8]} already exists in config, skipping addition.")

    src_name, dest_name, _, _ = get_language_names(users_config, hashed_user_id)
    await message.answer(f'{MESSAGES["/start"]}\n{src_name} ->> {dest_name}')


@router.message(Command(commands='change_language'))
async def change_language(message: Message):
    users_config = load_users_config()
    src_name, dest_name, _, _ = get_language_names(users_config, get_hashed_user_id(message))
    await message.answer(MESSAGES['/change_language'])
    await message.answer(f'Source: {src_name}', reply_markup=create_language_keyboard(bot_lang_from, prefix='FROM'))
    await message.answer(f'Destination: {dest_name}', reply_markup=create_language_keyboard(bot_lang_to, prefix='TO'))


@router.message(Command(commands='swap_language'))
async def swap_language(message: Message):
    user_id = str(message.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    users_config = load_users_config()
    src_name, dest_name, src_lang, dest_lang = get_language_names(users_config, hashed_user_id)
    if src_lang == 'auto':
        await message.answer(MESSAGES['/swap_language'])
    else:
        users_config[hashed_user_id]['src_lang'] = dest_lang
        users_config[hashed_user_id]['dest_lang'] = src_lang
        save_users_config(users_config)
        await message.answer(f'{MESSAGES["/configs"]}\n{dest_name} ->> {src_name}')


@router.message(Command(commands='help'))
async def help_message(message: Message):
    await message.answer(MESSAGES['/help'])


@router.message(Command(commands='configs'))
async def configs_message(message: Message):
    users_config = load_users_config()
    src_name, dest_name, _, _ = get_language_names(users_config, get_hashed_user_id(message))
    await message.answer(f'{MESSAGES["/configs"]}\n{src_name} ->> {dest_name}')


@router.message(Command(commands='get_stats'))
async def send_stats(message: Message):
    if message.from_user.id in config.tg_bot.admin_ids:
        cols, rows = get_stats()
        csv_data = stats_to_csv(cols, rows)
        file_name = generate_filename(rows)
        await message.answer_document(BufferedInputFile(csv_data.encode(), filename=file_name))
    else:
        await message.answer(MESSAGES['/get_stats'])


@router.message(F.content_type == ContentType.TEXT)
async def send_translation(message: Message):
    users_config = load_users_config()
    hashed_user_id = get_hashed_user_id(message)
    hashed_user_config = users_config.get(hashed_user_id, {})
    translated_text = translate(message.text,
                                **{lang: hashed_user_config.get(lang) for lang in ['src_lang', 'dest_lang']})
    save_stats(users_config)
    await message.answer(translated_text)


@router.callback_query(F.data.startswith('FROM'))
async def source_language(callback: CallbackQuery):
    language_code = callback.data.split('_')[-1]
    user_id = str(callback.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    users_config = load_users_config()
    current_src_lang = users_config[hashed_user_id]['src_lang']
    if current_src_lang != language_code:
        users_config[hashed_user_id]['src_lang'] = language_code
        language_name = next((lang for lang, code in bot_lang_from.items() if code == language_code))
        save_users_config(users_config)
        await callback.message.edit_text(f'Source: {language_name}',
                                         reply_markup=create_language_keyboard(bot_lang_from, prefix='FROM'))


@router.callback_query(F.data.startswith('TO'))
async def destination_language(callback: CallbackQuery):
    language_code = callback.data.split('_')[-1]
    user_id = str(callback.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    users_config = load_users_config()
    current_dest_lang = users_config[hashed_user_id]['dest_lang']
    if current_dest_lang != language_code:
        users_config[hashed_user_id]['dest_lang'] = language_code
        language_name = next((lang for lang, code in bot_lang_to.items() if code == language_code), None)
        save_users_config(users_config)
        await callback.message.edit_text(f'Destination: {language_name}',
                                         reply_markup=create_language_keyboard(bot_lang_to, prefix='TO'))
