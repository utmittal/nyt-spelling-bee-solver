import os
from pathlib import Path
import json

PROJECT_ROOT_PATH = str(Path(__file__).parent)


def get_latest_custom_dictionary_path() -> str:
    dicts = os.listdir(f'{PROJECT_ROOT_PATH}/dictionaries/custom')
    dicts.sort(reverse=True)
    return f'{PROJECT_ROOT_PATH}/dictionaries/custom/{dicts[0]}'


def get_benchmarking_dictionary_path() -> str:
    # Use the biggest dictionary for benchmarking
    return f'{PROJECT_ROOT_PATH}/dictionaries/raw/words_alpha.txt'


def write_words_to_dictionary(word_list: list[str], path: str) -> None:
    """
    Writes lowercase words in sorted order to specified file.

    :param word_list: List of words to write
    :param path: Path relative to dictionary directory
    """
    with open(f'{PROJECT_ROOT_PATH}/dictionaries/{path}', 'w+') as writefile:
        writefile.writelines(word.lower() + '\n' for word in sorted(word_list))


def _convert_categorized_json_to_wordlist_file() -> None:
    with open(f'{PROJECT_ROOT_PATH}/dictionaries/raw/2of12id.json') as f:
        json_words = json.load(f)
    word_list = []
    for key in json_words:
        word_list.extend(json_words[key])

    write_words_to_dictionary(word_list, 'raw/words_common.txt')


def _remove_small_words(dictionary: list[str]) -> list[str]:
    """
    Removes words smaller than 4 letters since NYT doesn't allow them.
    """
    return [w for w in dictionary if len(w) > 3]
