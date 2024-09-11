with open('dictionary/words_alpha.txt') as f:
    words = f.read().splitlines()

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


analyze_dictionary(words)
