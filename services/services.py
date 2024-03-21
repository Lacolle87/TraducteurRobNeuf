from googletrans import Translator

translator = Translator()


def translate(text: str | None, src_lang='auto', dest_lang='en') -> str:
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text
