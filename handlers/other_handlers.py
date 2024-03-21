from aiogram import Router, F
from aiogram.types import Message, ContentType

router = Router()


@router.message(F.content_type != ContentType.TEXT)
async def send_echo(message: Message):
    await message.reply(text='didn`t get it mate, try to type text')
