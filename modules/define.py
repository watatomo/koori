import cutlet
import json.decoder

from jisho_api.word import Word

katsu = cutlet.Cutlet()

async def get_romaji(string):
    return katsu.romaji(string)

def get_definitions(text):
    max_retries = 20
    retries = 0

    while retries < max_retries:
        try:
            print('Getting definitions...')
            r = Word.request(text)
            definitions = []
            for sense in r.data[0].senses:
                definitions.extend(sense.english_definitions)
            return definitions
        except json.decoder.JSONDecodeError as json_error:
            print("Retrying...")
            retries += 1
        except Exception as e:
            return ["Invalid."]

    return ["Invalid."]

def process_word(word):
    if word.feature.pos1 == '補助記号':
        return None
    else:
        definitions = get_definitions(word.surface)
        return (word.surface, definitions)