import hashlib
from googletrans import Translator

translator = Translator()


def translate(text: str | None, src_lang='auto', dest_lang='en') -> str:
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text


def hash_user_id(user_id):
    user_id_bytes = str(user_id).encode('utf-8')
    hash_object = hashlib.sha256(user_id_bytes)
    hashed_user_id = hash_object.hexdigest()
    return hashed_user_id
