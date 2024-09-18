import string
import time
import os
from dictionary_utils import get_latest_custom_dictionary_path


def _validate_character_args(center: str, others: str):
    if len(others) > len(set(others)):
        raise ValueError("List of other characters cannot contain repeated characters.")
    if len(set(others)) != 6:
        raise ValueError("There should be exactly 6 other characters.")
    if len(center) != 1:
        raise ValueError("There can be only one center character.")
    if center in others:
        raise ValueError("Central character cannot be in list of other characters.")


def get_bee_solutions_naive(center: str, others: str | list[str], dictionary: list[str]) -> list[str]:
    """
    Naive approach. Simply iterate through whole dictionary and check if the word could be formed from the given
    letters.

    :param center: Central character that must appear in word. Expected to be of length = 1
    :param others: List of other characters that must appear in word. Excludes center character and must be of length
    = 6
    :param dictionary: list of words to search in
    :return: List of solutions
    """
    _validate_character_args(center, others)

    valid_bee_words = []
    letter_set = set(others + center)
    for word in dictionary:
        if center in word:
            if set(word) <= letter_set:
                valid_bee_words.append(word)

    return valid_bee_words


def _preprocess_get_bit_to_word_dict(dictionary: list[str]) -> dict[int: [str]]:
    """
    Generates a dictionary where the keys are the bit representation of the word (as an integer) and the values are
    a list of corresponding words. Bit representations ignore letter ordering and letter duplicates. So a single bit
    representation may have multiple corresponding words.

    :param dictionary: list of words
    :return: dict of bit representation to list of words
    """
    bit_dict = {}
    for word in dictionary:
        word_bits = ['0'] * 26
        letters = set(word)
        for c in letters:
            word_bits[string.ascii_lowercase.index(c)] = '1'
        word_bits = int(''.join(word_bits), 2)

        # anagrams and words with repeated letters will have the same bit representation
        if word_bits in bit_dict:
            bit_dict[word_bits].append(word)
        else:
            bit_dict[word_bits] = [word]

    return bit_dict


def get_bee_solutions_bitwise(center: str, others: str, bit_dictionary: dict[int: str]) -> list[str]:
    """
    Uses bit operations to check if a word is valid.

    Each word is a bit array of 26 bits, where each bit represents a letter from the alphabet. The central character
    and other characters are also represented in this manner. We can then derive a bit equation to check whether the
    word is valid. Given the high number of comparisons that we need to perform, this should be faster than the naive
    approach.

    Note: Python doesn't have a native bit class/type. We could use a list of booleans but bit operations in integers
    is much faster in python (and supported directly).

    :param center: Central character that must appear in word. Length = 1
    :param others: Other characters that must appear in word. Excludes center character and must be of length = 6
    :param bit_dictionary: Dictionary of words to look in, where the keys are the bit representations of the word and
    the values are the string representation of the words
    :return: list of solutions
    """
    _validate_character_args(center, others)

    """
    Truth table to derive a SoP equation. SoP is better than PoS here I think because we have more 0 terms (though I 
    guess I could always flip that if I was using PoS). 
    
    Note: This truth table is for the individual bits. Each bit can be thought of as a letter where 0 means the letter
    is absent and 1 means it's present
    
    W: word we are checking
    C: center letter that must always be present in the word
    O: other letters that should be optionally present in the word
    R: result where we want the value to be 1 if this combination invalidates the word

        W   C   O   R   notes
        ---------------------
        0   0   0   0   Letter absent in word, center and others. Word is valid.
        0   0   1   0   Letter present only in others. Word is valid.
        0   1   0   1   Letter present only in center. Hence, word is not valid
        0   1   1   0   Letter present in center and others. Not possible, so R=0 to reduce the number of terms.
        1   0   0   1   Letter present in word but not in center or others. Word is invalid.
        1   0   1   0   Letter present in word and in others. Word is valid.
        1   1   0   0   Letter present in word and in center. Word is valid.
        1   1   1   0   Letter present in word, center and others. Not possible, so R=0 to reduce the number of terms.

    SoP = ((not W) and C and (not O)) OR (W and (not C) and (not O))
        = (~W & C & ~O) | (W & ~C & ~O)
        = ~O & ((~W & C) | (W & ~C))
    """

    not_mask = 67108863  # int representation of binary number with 26 1s

    center_bits = ['0'] * 26
    center_bits[string.ascii_lowercase.index(center)] = '1'
    center_bits = int(''.join(center_bits), 2)
    # ints in python are infinite precision, so ~ gives us an infinite number of leading 1s at the front. We fix this
    # by ANDing with a mask of 26 1s
    center_bits_negated = ~center_bits & not_mask
    other_bits_negated = ['0' if l in others else '1' for l in string.ascii_lowercase]
    other_bits_negated = int(''.join(other_bits_negated), 2)

    valid_bee_words = []
    for word_bits in bit_dictionary:
        word_bits_negated = ~word_bits & not_mask
        result = other_bits_negated & ((word_bits_negated & center_bits) | word_bits & center_bits_negated)
        if result == 0:
            valid_bee_words.extend(bit_dictionary[word_bits])

    return valid_bee_words


def _preprocess_get_prefix_tree(dictionary: list[str]) -> dict[str: set[str]]:
    """
    Converts the list of words into a prefix tree (trie) where each node is a string prefix and each child represents
    a prefix that can be formed by adding a letter to the parent. I.e. Node 'ro' will have a path to 'rob' and a
    path to 'rot' etc. Small sample of the tree:
            r
          /  \\
       ro     ra
     /   \\     \\
    rot   rob    rat

    This tree is represented as a prefix dictionary, where the keys are all possible prefixes and the values are the
    set of possible next characters corresponding to that prefix.

    :param dictionary: list of words to use
    :return: dictionary of prefix to list of next characters
    """
    big_massive_dict = {}

    for word in dictionary:
        word_with_end = word + "$"  # gives us an ending character to know the word has finished
        word_length = len(word_with_end)
        for i in range(1, word_length):
            prefix, next_char = word_with_end[:i], word_with_end[i]
            if prefix not in big_massive_dict:
                big_massive_dict[prefix] = {next_char}
            else:
                big_massive_dict[prefix].add(next_char)

    # starting node
    big_massive_dict[''] = set(string.ascii_lowercase)

    return big_massive_dict


def _traverse_prefix_tree(prefix: str, center: str, valid_letters: str | set[str],
                          prefix_tree: dict[str: set[str]]) -> list[str]:
    """
    Recursive function to traverse through prefix tree to find all words formed by the given letters.

    :param prefix: Current prefix string.
    :param center: Central letter that must appear in a valid word
    :param valid_letters: List of letters that we are trying to form words from.
    :param prefix_tree: Prefix tree as a dict of prefixes to valid next characters
    :return:
    """
    valid_words = []
    next_char_set = prefix_tree[prefix]

    # can't form a valid word
    if center not in prefix and center not in next_char_set:
        return valid_words

    if '$' in next_char_set and center in prefix:
        valid_words.append(prefix)

    for letter in next_char_set:
        if letter in valid_letters:
            valid_words.extend(_traverse_prefix_tree(prefix + letter, center, valid_letters, prefix_tree))

    return valid_words


def get_bee_solutions_prefix_tree(center: str, others: str | list[str], prefix_tree: dict[str: set[str]]) -> list[
    str]:
    """
    Uses a prefix tree to find all valid words. Each node in the tree is a string prefix and each path is a valid letter
    that can succeed the prefix.

    :param center: Central character that must appear in word. Length = 1
    :param others: Other characters that must appear in word. Excludes center character and must be of length = 6
    :param prefix_tree: dict of prefix strings to corresponding valid succeeding characters
    :return: list of solutions
    """
    _validate_character_args(center, others)

    return _traverse_prefix_tree('', center, set(center + others), prefix_tree)


type NestedStrDict = dict[str: NestedStrDict | None]


def _preprocess_get_radix_tree(suffix_list: list[str], curr_dict: NestedStrDict) -> NestedStrDict:
    """
    Converts the list of words into a tree where each node is a letter and each child is a valid succeeding
    letter that will eventually form a word. This is essentially a radix tree. A small sample of this tree might look
    like this:
         r
        /
       o
     /  \\
    t     b

    The tree is represented by a nested dictionary where the key is a letter and the corresponding value is a
    dictionary whose keys are the possible next letters. The end of a word is represented by the character '$' and
    the corresponding value to '$' itself is None (but it's never actually read).

    :param suffix_list: the current list of suffixes to process
    :param curr_dict: the dictionary for the current prefix being processed
    :return: Generated tree represented by a NestedStrDict
    """
    if suffix_list == ['']:
        curr_dict['$'] = None  # '$' character to indicate end of word
        return curr_dict

    for suffix in suffix_list:
        first_char = suffix[0]

        if first_char in curr_dict:
            curr_dict[first_char] = _preprocess_get_radix_tree([suffix[1:]], curr_dict[first_char])
        else:
            curr_dict[first_char] = _preprocess_get_radix_tree([suffix[1:]], {})

    return curr_dict


def _traverse_radix_tree(current_prefix: str, curr_dict: NestedStrDict, center, valid_letters: str | list[str]) -> \
        list[str]:
    """
    Recursive function to traverse through the radix tree as represented by a NestedStrDict.

    :param current_prefix: Current prefix string
    :param curr_dict: Current NestedStrDict representing all possible next characters for the current prefix
    :param valid_letters: The list of valid letters from which we can form words
    :return: list of valid words formed from the letters
    """
    valid_words = []
    if '$' in curr_dict and center in current_prefix:
        valid_words.append(current_prefix)

    for letter in curr_dict:
        if letter in valid_letters:
            valid_words.extend(_traverse_radix_tree(current_prefix + letter, curr_dict[letter], center, valid_letters))

    return valid_words


def get_bee_solutions_radix_tree(center: str, others: str, radix_tree: NestedStrDict) -> list[str]:
    """
    Uses a tree to find all valid words. Each node is a letter and each child is a valid succeeding letter that will
    eventually form a word.

    Note: We don't check for the necessary character during the recursion itself because for some reason that is
    slower? Instead, we just do a final pass at the end before returning the list.

    :param center: Central character that must appear in word. Length = 1
    :param others: Other characters that must appear in word. Excludes center character and must be of length = 6
    :param radix_tree: word tree
    :return: list of solutions
    """
    _validate_character_args(center, others)

    valid_bee_words = _traverse_radix_tree('', radix_tree, center, center + others)

    return valid_bee_words


def pretty_print_solution(sol_list, center, others, uncommon=False):
    sol_list.sort()

    with open(get_latest_custom_dictionary_path()) as reader:
        common_words = reader.read().splitlines()

    common_sols = [sol for sol in sol_list if sol in common_words]
    other_sols = [sol for sol in sol_list if sol not in common_words]

    print("Spelling Bee Solution - [" + center.upper() + " | " + ' '.join(c.upper() for c in others) + "]:")
    print("\tCommon Words - " + str(len(common_sols)) + ":")
    print('\n'.join([str("\t\t" + sol) for sol in common_sols]))
    if uncommon:
        print("\tOther Words - " + str(len(other_sols)) + ":")
        print('\n'.join([str("\t\t" + sol) for sol in other_sols]))


def measure_execution_time(function, *args, iterations=1):
    total_time = 0
    result = None
    for i in range(0, iterations):
        start_time = time.time()
        result = function(*args)
        end_time = time.time()

        total_time += (end_time - start_time)

    print("Average execution time (" + str(iterations) + " iterations): " + str(total_time / iterations) + " seconds")
    return result


with open('dictionaries/processed/words_bee.txt') as f:
    words = f.read().splitlines()

# note: this combo seems to be the combo with the highest number of words
# in the history of nyt spelling bee
time_iters = 10000
today_center = 'o'
today_others = "ctpnme"

# time_iters = 1
# today_center = 'r'
# today_others = "inpbug"

# print("Naive")
# solution_words = measure_execution_time(get_bee_words_naive,today_center,today_others,words, iterations = time_iters)
# # pretty_print_solution(solution_words,today_center,today_others)
#
# print("Bitwise")
# bit_to_string_dict = measure_execution_time(_preprocess_get_bit_to_word_dict, words)
# solution_words = measure_execution_time(get_bee_solutions_bitwise, today_center, today_others, bit_to_string_dict,
#                                         iterations=time_iters)
# pretty_print_solution(solution_words, today_center, today_others)
#
print("Graph")
letter_graph = measure_execution_time(_preprocess_get_prefix_tree, words)
solution_words = measure_execution_time(get_bee_solutions_prefix_tree, today_center, today_others, letter_graph,
                                        iterations=time_iters)
# pretty_print_solution(solution_words, today_center, today_others)

print("Nested Graph")
nested_dict = measure_execution_time(_preprocess_get_radix_tree, words, {})
solution_words = measure_execution_time(get_bee_solutions_radix_tree, today_center, today_others, nested_dict,
                                        iterations=time_iters)
# pretty_print_solution(solution_words, today_center, today_others)
