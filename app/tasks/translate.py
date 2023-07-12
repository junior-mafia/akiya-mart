from googletranslate import translate
from app.tasks.repo import (
    select_details_missing_translation,
    insert_translations,
)
import html


CHUNK_SIZE = 100


def translate_from_japanese(text):
    translation = translate(text, "en", "ja", client="te_lib")
    escaped_translation = html.unescape(translation)
    return escaped_translation


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def translation_task(session):
    details = select_details_missing_translation(session)
    for chunk in chunker(details, CHUNK_SIZE):
        translated_details = []
        for row in chunk:
            description = "\n\n".join(map(translate_from_japanese, row["description"]))
            remarks = translate_from_japanese(row["remarks"])
            address = translate_from_japanese(row["address"])
            item = {
                "bukken_id": row["bukken_id"],
                "source": row["source"],
                "description": description,
                "remarks": remarks,
                "address": address,
            }
            translated_details.append(item)
        print(
            "AKIYA-MART-TASKS: translation: INSERTING {n} RECORDS".format(
                n=len(translated_details)
            )
        )
        insert_translations(session, translated_details)
