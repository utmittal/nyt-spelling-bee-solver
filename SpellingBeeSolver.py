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
    for i in range(0,iterations):
        start_time = time.time()
        result = function(*args)
        end_time = time.time()

        total_time += (end_time - start_time)

    print("Average execution time (" + str(iterations) + " iterations): " + str(total_time/iterations) + " seconds")
    return result

with open('dictionary/words_bee.txt') as f:
    words = f.read().splitlines()

# note: this combo seems to be the combo with the highest number of words
# in the history of nyt spelling bee
today_center = 'o'
today_others = "ctpnme"
# solution_words = get_bee_words_naive(today_center,today_others,words)
# pretty_print_solution(solution_words,today_center,today_others)

measure_execution_time(get_bee_words_naive,today_center,today_others,words, iterations = 100)
