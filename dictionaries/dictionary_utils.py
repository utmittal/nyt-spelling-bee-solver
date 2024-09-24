import collections
import json
import os
from pathlib import Path

from util.project_path import project_path


def get_latest_custom_dictionary() -> list[str]:
    """
    :return: list of words from latest custom dictionary
    """
    dicts = os.listdir(project_path('dictionaries/custom'))
    dicts.sort(reverse=True)
    return get_dictionary_from_path(f'dictionaries/custom/{dicts[0]}')


def get_benchmarking_dictionary() -> list[str]:
    """
    :return: list of words from dictionary used for benchmarking
    """
    # Use the biggest dictionary for benchmarking
    return get_dictionary_from_path('dictionaries/raw/words_alpha.txt')


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
    write_words_to_dictionary(word_list, f'dictionaries/custom/nyt_spelling_bee_dictionary.txt')


def analyze_dictionary(dictionary: list[str]) -> None:
    """
    Prints various stats for a given list of words. Useful for analyzing different dictionaries to figure out which
    to use in the project.

    :param dictionary: list of words
    """
    longest_words = []
    longest_len = 0
    shortest_words = []
    shortest_len = 10000  # some big number
    words_with_most_single_repeated_letter = []
    single_repeated_letter_count = 0
    words_with_most_repeated_letters = []
    repeated_letters_count = 0
    for word in dictionary:
        wl = len(word)
        if wl > longest_len:
            longest_words = [word]
            longest_len = wl
        elif wl == longest_len:
            longest_words.append(word)

        if wl < shortest_len:
            shortest_words = [word]
            shortest_len = wl
        elif wl == shortest_len:
            shortest_words.append(word)

        char_counter = collections.Counter(word)
        for key in char_counter:
            if char_counter[key] > single_repeated_letter_count:
                words_with_most_single_repeated_letter = [word]
                single_repeated_letter_count = char_counter[key]
            elif char_counter[key] == single_repeated_letter_count:
                words_with_most_single_repeated_letter.append(word)

        total_repeated_letters = 0
        for key in char_counter:
            # Only interested in repeating letters
            if char_counter[key] > 1:
                total_repeated_letters += char_counter[key]
        if total_repeated_letters > repeated_letters_count:
            words_with_most_repeated_letters = [word]
            repeated_letters_count = total_repeated_letters
        elif total_repeated_letters == repeated_letters_count:
            words_with_most_repeated_letters.append(word)

    print("Dictionary Analysis - Note: Max 10 sample words printed in each category")
    print(f"\tTotal Words: {str(len(dictionary))}")
    print(f"\tShortest Words ({str(shortest_len)}):\n{'\n'.join([str("\t\t" + w) for w in shortest_words[:10]])}")
    print(f"\tLongest Words ({str(longest_len)}):\n{'\n'.join([str("\t\t" + w) for w in longest_words[:10]])}")
    print(
        f"\tWords with most single repeating letter ({str(single_repeated_letter_count)}):\n"
        f"{'\n'.join([str("\t\t" + w) for w in words_with_most_single_repeated_letter[:10]])}")
    print(
        f"\tWords with most total repeating letters ({str(repeated_letters_count)}):\n"
        f"{'\n'.join([str("\t\t" + w) for w in words_with_most_repeated_letters[:10]])}")


def _convert_categorized_json_to_wordlist_file() -> None:
    with open(project_path('dictionaries/raw/2of12id.json'), 'r') as f:
        json_words = json.load(f)
    word_list = []
    for key in json_words:
        word_list.extend(json_words[key])

    write_words_to_dictionary(word_list, 'dictionaries/raw/words_common.txt')


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
