import os


def get_latest_custom_dictionary_path():
    dics = os.listdir('dictionaries/custom')
    dics.sort(reverse=True)
    return 'dictionaries/custom/' + dics[0]


def get_benchmarking_dictionary_path():
    # Use biggest dictionary for benchmarking
    return 'dictionaries/raw/words_alpha.txt'
