
def get_bee_words_naive(center, others, dictionary):
    """
    Naive approach. Simply iterate and check through whole dictionary.

    :param center: Central character that must appear in word
    :param others: List of other characters that must appear in word
    :param dictionary: list of words to search in
    :return: List of bee words
    """
    if len(others) > len(set(others)):
        raise ValueError("List of other characters cannot contain repeated characters.")
    if center in others:
        raise ValueError("Central character cannot be in list of other characters.")

    valid_bee_words = []
    letter_set = set(others+center)
    for word in dictionary:
        if center in word:
            if set(word) <= letter_set:
                valid_bee_words.append(word)

    return valid_bee_words

def pretty_print_solution(sol_list, center, others):
    sol_list.sort()

    with open('dictionary/words_common_bee.txt') as reader:
        common_words = reader.read().splitlines()

    common_sols = [sol for sol in sol_list if sol in common_words]
    other_sols = [sol for sol in sol_list if sol not in common_words]

    print("Spelling Bee Solution - [" + center.upper() + " | " + ' '.join(c.upper() for c in others) + "]:")
    print("\tCommon Words - " + str(len(common_sols)) + ":")
    print('\n'.join([str("\t\t" + sol) for sol in common_sols]))
    print("\tOther Words - " + str(len(other_sols)) + ":")
    print('\n'.join([str("\t\t" + sol) for sol in other_sols]))

with open('dictionary/words_bee.txt') as f:
    words = f.read().splitlines()

solution_words = get_bee_words_naive('e',"acfpty",words)
pretty_print_solution(solution_words,'e','acfpty')