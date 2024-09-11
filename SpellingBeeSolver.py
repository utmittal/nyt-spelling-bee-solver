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

    print("Longest Words:\n" + ('\n'.join([str("\t" + w + " : " + str(len(w))) for w in longest_words])))
    print("Shortest Words:\n" + ('\n'.join([str("\t" + w + " : " + str(len(w))) for w in shortest_words])))

# with open('dictionary/words_alpha.txt') as f:
#     words = f.read().splitlines()
# gen_bee_dictionary(words)

with open('dictionary/words_bee.txt') as f:
    words = f.read().splitlines()
analyze_dictionary(words)