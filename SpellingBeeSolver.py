
def print_bee_words_naive(center, others, dictionary):
    """
    Naive approach. Simply iterate and check through whole dictionary.

    :param center: Central character that must appear in word
    :param others: List of other characters that must appear in word
    :param dictionary: list of words to search in
    :return: None
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
    valid_bee_words.sort()

    print("Spelling Bee Solution - [" + center.upper() + " | " + ' '.join(c.upper() for c in others) + "] - " + str(len(valid_bee_words)) + " words:")
    print('\n'.join([str("\t" + sol) for sol in valid_bee_words]))

with open('dictionary/words_bee.txt') as f:
    words = f.read().splitlines()

print_bee_words_naive('e',"acfpty",words)