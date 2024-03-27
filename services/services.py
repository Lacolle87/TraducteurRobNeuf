import logging
import hashlib
from googletrans import Translator

translator = Translator()


def translate(text: str | None, src_lang='auto', dest_lang='en') -> str:
    try:
        translation = translator.translate(text, src=src_lang, dest=dest_lang)
        logging.info(f"Translated text from {src_lang} to {dest_lang}")
        return translation.text
    except Exception as e:
        logging.error(f"Error translating text: {e}")


def hash_user_id(user_id: str) -> str:
    user_id_bytes = user_id.encode('utf-8')
    hash_object = hashlib.sha256(user_id_bytes)
    hashed_user_id = hash_object.hexdigest()
    return hashed_user_id


def hash_file_data(data: str) -> str:
    try:
        file_hash = hashlib.sha256()
        for line in data:
            file_hash.update(line.encode('utf-8'))
        logging.info("Hashed file data successfully")
        return file_hash.hexdigest()
    except Exception as e:
        logging.error(f"Error hashing file data: {e}")
