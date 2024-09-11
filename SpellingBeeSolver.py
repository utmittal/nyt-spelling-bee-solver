import collections


def gen_bee_dictionary(dictionary):
    """
    NYT spelling bee only allows words longer than 3 characters
    """
    bee_dictionary = [w for w in dictionary if len(w) > 3]
    with open('dictionary/words_bee.txt', 'w+') as writefile:
        writefile.writelines(word + '\n' for word in bee_dictionary)

def analyze_dictionary(dictionary):
    longest_words = []
    longest_len = 0
    shortest_words = []
    shortest_len = 10000    # some big number
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
    print("\tTotal Words: " + str(len(dictionary)))
    print("\tShortest Words (" + str(shortest_len) + "):\n" + ('\n'.join([str("\t\t" + w) for w in shortest_words[:10]])))
    print("\tLongest Words (" + str(longest_len) + "):\n" + ('\n'.join([str("\t\t" + w) for w in longest_words[:10]])))
    print("\tWords with most single repeating letter (" + str(single_repeated_letter_count) + "):\n" + ('\n'.join([str("\t\t" + w) for w in words_with_most_single_repeated_letter[:10]])))
    print("\tWords with most total repeating letters (" + str(repeated_letters_count) + "):\n" + ('\n'.join([str("\t\t" + w) for w in words_with_most_repeated_letters[:10]])))

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

# with open('dictionary/words_alpha.txt') as f:
#     words = f.read().splitlines()
# gen_bee_dictionary(words)

with open('dictionary/words_bee.txt') as f:
    words = f.read().splitlines()
# analyze_dictionary(words)

print_bee_words_naive('e',"acfpty",words)