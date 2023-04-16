import re

def remove_japanese(text):
    english_and_symbols = re.sub(r'[^\x00-\x7F]+', '', text)
    if english_and_symbols == "":
        english_and_symbols="not english name image"
    return english_and_symbols