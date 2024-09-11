import string
import time

def check_bee_words_args(center, others):
    if len(others) > len(set(others)):
        raise ValueError("List of other characters cannot contain repeated characters.")
    if center in others:
        raise ValueError("Central character cannot be in list of other characters.")

def get_bee_words_naive(center, others, dictionary):
    """
    Naive approach. Simply iterate and check through whole dictionary.

    :param center: Central character that must appear in word
    :param others: List of other characters that must appear in word
    :param dictionary: list of words to search in
    :return: List of bee words
    """
    check_bee_words_args(center, others)

    valid_bee_words = []
    letter_set = set(others+center)
    for word in dictionary:
        if center in word:
            if set(word) <= letter_set:
                valid_bee_words.append(word)

    return valid_bee_words

def preprocess_get_bit_to_word_dict(dictionary):
    bit_dict = {}
    for word in dictionary:
        bits = ['0'] * 26
        chars = set(word)
        for c in chars:
            bits[string.ascii_lowercase.index(c)] = "1"

        bits = int(''.join(bits),2)
        if bits in bit_dict:
            bit_dict[bits].append(word)
        else:
            bit_dict[bits] = [word]

    return bit_dict

def preprocess_get_bit_to_negation_dict(dictionary):
    negated_dict = {}
    for word in dictionary:
        bits = ['0'] * 26
        negated = ['1'] * 26
        chars = set(word)
        for c in chars:
            bits[string.ascii_lowercase.index(c)] = "1"
            negated[string.ascii_lowercase.index(c)] = "0"

        bits = int(''.join(bits),2)
        negated = int(''.join(negated),2)
        negated_dict[bits] = negated

    return negated_dict

def get_bee_words_bitwise(center, others, dictionary, word_to_negated_word):
    check_bee_words_args(center, others)

    """
    truth table where word refers to the word we are checking. Center must always be present in the word.
    Others should be optionally present in the word. We want the value to be greater than 0 if the word isnt valid.

        word    center  others  result  minterms
        0       0       0       0
        0       0       1       0
        0       1       0       1       ((NOT word) AND center AND (NOT others))
        0       1       1       0   # technically should never happen, so we put 0 to reduce our sum of products
        1       0       0       1       (word AND (NOT center) AND (NOT others))
        1       0       1       0
        1       1       0       0
        1       1       1       0   # technically should never happen, so we put 0 to reduce our sum of products

        sop = ((NOT word) AND center AND (NOT others)) + (word AND (NOT center) AND (NOT others))
            = (~W C ~O) + (W ~C ~O)

        This is why we calculate the negated words in advance, so that we don't have to waste time on it in this
        function. Because NOT in python is weird. Should probably figured out how it works actually.
    """

    # We need to perform the bit operation [word OR (NOT letters)] to get the right answers
    # However, bitwise not in python is weird because ints can be arbitrarily long
    # Instead of figuring out how the not works, we just generate the NOT of letters and center
    # in the first place. We have to do that work anyway, so this doesn't take extra time
    # If anything, it takes less time.
    other_bits_negated = ['1'] * 26
    for o in others:
        other_bits_negated[string.ascii_lowercase.index(o)] = "0"
    other_bits_negated = int(''.join(other_bits_negated),2)
    center_bits = ['0'] * 26
    center_bits_negated = ['1'] * 26
    center_bits[string.ascii_lowercase.index(center)] = "1"
    center_bits_negated[string.ascii_lowercase.index(center)] = "0"
    center_bits = int(''.join(center_bits),2)
    center_bits_negated = int(''.join(center_bits_negated),2)

    valid_bee_words = []
    for word_bits in dictionary:
        result = (word_to_negated_word[word_bits] & center_bits & other_bits_negated) | (word_bits & center_bits_negated & other_bits_negated)
        if result == 0:
            valid_bee_words.extend(dictionary[word_bits])

    return valid_bee_words


def pretty_print_solution(sol_list, center, others, uncommon = False):
    sol_list.sort()

    with open('dictionary/words_common_bee.txt') as reader:
        common_words = reader.read().splitlines()

    common_sols = [sol for sol in sol_list if sol in common_words]
    other_sols = [sol for sol in sol_list if sol not in common_words]

    print("Spelling Bee Solution - [" + center.upper() + " | " + ' '.join(c.upper() for c in others) + "]:")
    print("\tCommon Words - " + str(len(common_sols)) + ":")
    print('\n'.join([str("\t\t" + sol) for sol in common_sols]))
    if uncommon:
        print("\tOther Words - " + str(len(other_sols)) + ":")
        print('\n'.join([str("\t\t" + sol) for sol in other_sols]))

def measure_execution_time(function, *args, iterations = 1):
    total_time = 0
    result = None
    for i in range(0,iterations):
        start_time = time.time()
        result = function(*args)
        end_time = time.time()

        total_time += (end_time - start_time)

    print("Average execution time (" + str(iterations) + " iterations): " + str(total_time/iterations) + " seconds")
    return result

with open('dictionary/words_bee.txt') as f:
    words = f.read().splitlines()

time_iters = 500
# note: this combo seems to be the combo with the highest number of words
# in the history of nyt spelling bee
today_center = 'o'
today_others = "ctpnme"
# solution_words = get_bee_words_naive(today_center,today_others,words)
# pretty_print_solution(solution_words,today_center,today_others)
measure_execution_time(get_bee_words_naive,today_center,today_others,words, iterations = time_iters)

# bit_dictionary = preprocess_get_bit_to_word_dict(words)
# negated_dictionary = preprocess_get_bit_to_negation_dict(words)
# solution_words = get_bee_words_bitwise(today_center, today_others, bit_dictionary, negated_dictionary)
# pretty_print_solution(solution_words, today_center, today_others)
bit_dictionary = measure_execution_time(preprocess_get_bit_to_word_dict,words, iterations = time_iters)
negated_dictionary = measure_execution_time(preprocess_get_bit_to_negation_dict,words, iterations = time_iters)
solution_words = measure_execution_time(get_bee_words_bitwise,today_center, today_others, bit_dictionary, negated_dictionary, iterations = time_iters)
# pretty_print_solution(solution_words, today_center, today_others)
