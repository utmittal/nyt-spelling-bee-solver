import os


def get_latest_custom_dictionary_path():
    dics = os.listdir('dictionaries/custom')
    dics.sort(reverse=True)
    return 'dictionaries/custom/' + dics[0]
