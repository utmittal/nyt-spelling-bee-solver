from pathlib import Path

from util.project_path import project_path


def get_custom_dictionary() -> list[str]:
    """
    :return: list of words from custom dictionary
    """
    return get_dictionary_from_path(f'data/custom/nyt_spelling_bee_dictionary.txt')


def get_benchmarking_dictionary() -> list[str]:
    """
    :return: list of words from dictionary used for benchmarking
    """
    # Use the biggest dictionary for benchmarking
    return get_dictionary_from_path('data/raw_word_lists/words_alpha.txt')


def get_dictionary_from_path(path: str | Path) -> list[str]:
    """
    Returns a list of words from the file specified by path.
    :param path: Path relative to project root.
    :return: List of words
    """
    with open(project_path(path), 'r') as f:
        return f.read().splitlines()


def write_words_to_dictionary(word_list: list[str] | set[str], path: str) -> None:
    """
    Writes lowercase words in sorted order to specified file.

    Also removes any words smaller than 4 letters and any words that have more than 7 unique letters.

    :param word_list: List of words to write
    :param path: Path relative to project root
    """
    word_list = list(set(word_list))  # remove dupes
    word_list = _remove_small_words(word_list)
    word_list = _remove_long_words(word_list)
    word_list = _remove_impossible_words(word_list)
    with open(project_path(path), 'w+') as writefile:
        writefile.writelines(word.lower() + '\n' for word in sorted(word_list))


def write_words_to_custom_dictionary(word_list: list[str] | set[str]) -> None:
    """
    Writes words to the custom NYT spelling bee dictionary.
    """
    write_words_to_dictionary(word_list, f'data/custom/nyt_spelling_bee_dictionary.txt')


def _remove_small_words(dictionary: list[str]) -> list[str]:
    """
    Removes words smaller than 4 letters since NYT doesn't allow them.
    """
    return [w for w in dictionary if len(w) > 3]


def _remove_long_words(dictionary: list[str]) -> list[str]:
    """
    Removes words longer than 19 letters since NYT doesn't allow them.
    """
    return [w for w in dictionary if len(w) < 20]


def _remove_impossible_words(dictionary: list[str]) -> list[str]:
    """
    Removes any words with more than 7 unique letters since that's impossible for a NYT Spelling Bee puzzle.
    """
    return [w for w in dictionary if len(set(w)) <= 7]


def add_words_to_custom(new_words: list[str] | set[str]) -> None:
    """
    Adds words to custom dictionary.
    """
    updated_word_set = set(get_custom_dictionary())
    updated_word_set.update(new_words)
    write_words_to_custom_dictionary(updated_word_set)


def delete_words_from_custom(delete_list: list[str] | set[str]):
    """
    Deletes words from custom dictionary.
    """
    updated_word_set = set(get_custom_dictionary())
    updated_word_set = updated_word_set - set(delete_list)
    write_words_to_custom_dictionary(updated_word_set)
