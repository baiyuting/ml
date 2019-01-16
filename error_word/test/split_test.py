from error_word.detect_error_model import people_words_characters, one_character_model

with open("split", 'r', encoding='utf-8') as fp:
    lines = fp.readlines()

one_character_model(lines)