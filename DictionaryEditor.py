import os
from datetime import datetime


def get_latest_custom_dictionary_path():
    dics = os.listdir('dictionaries/custom')
    dics.sort(reverse=True)
    return 'dictionaries/custom/' + dics[0]


def get_current_words():
    with open(get_latest_custom_dictionary_path(), 'r') as f:
        words = f.read().splitlines()
    return words


def add_new_words(new_words):
    updated_word_set = set(get_current_words())
    updated_word_set.update(new_words)
    with open('dictionaries/custom/nyt_spelling_bee_dictionary_' + datetime.now().strftime('%Y%m%d'), 'w+') as f:
        f.writelines(word + '\n' for word in updated_word_set if len(word) > 3)


def delete_words(words):
    updated_word_set = set(get_current_words())
    for word in words:
        updated_word_set.remove(word)
    with open('dictionaries/custom/nyt_spelling_bee_dictionary_' + datetime.now().strftime('%Y%m%d'), 'w+') as f:
        f.writelines(word + '\n' for word in updated_word_set if len(word) > 3)


add_new_words([])
delete_words(["balboa"])
