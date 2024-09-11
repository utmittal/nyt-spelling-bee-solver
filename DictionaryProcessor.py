import collections
import json

def gen_bee_dictionary(dictionary, path):
    """
    NYT spelling bee only allows words longer than 3 characters
    """
    bee_dictionary = [w for w in dictionary if len(w) > 3]
    with open(path, 'w+') as writefile:
        writefile.writelines(word + '\n' for word in bee_dictionary)

def convert_categorized_json_to_wordlist_file():
    with open('dictionary/2of12id.json') as f:
        json_words = json.load(f)
    word_list = []
    for key in json_words:
        word_list.extend(json_words[key])

    with open('dictionary/words_common.txt','w+') as writefile:
        writefile.writelines(word + '\n' for word in word_list)

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

# with open('dictionary/words_alpha.txt') as f:
#     words = f.read().splitlines()
# gen_bee_dictionary(words)

# analyze_dictionary(words)

# convert_categorized_json_to_wordlist_file()
with open('dictionary/words_common.txt') as f:
    words = f.read().splitlines()
gen_bee_dictionary(words,'dictionary/words_common_bee.txt')