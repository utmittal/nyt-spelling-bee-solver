import os
from datetime import datetime
from SpellingBeeSolver import get_bee_words_graph_inception, preprocess_graph_inception_solution, \
    get_latest_custom_dictionary_path


def get_latest_custom_dictionary_path():
    dics = os.listdir('dictionaries/custom')
    dics.sort(reverse=True)
    return 'dictionaries/custom/' + dics[0]


def get_current_words():
    with open(get_latest_custom_dictionary_path(), 'r') as f:
        words = f.read().splitlines()
    return words


def add_new_words(new_words):
    updated_word_set = set(get_current_words())
    updated_word_set.update(new_words)
    with open('dictionaries/custom/nyt_spelling_bee_dictionary_' + datetime.now().strftime('%Y%m%d'), 'w+') as f:
        f.writelines(word + '\n' for word in updated_word_set if len(word) > 3)


def delete_words(words):
    updated_word_set = set(get_current_words())
    for word in words:
        updated_word_set.remove(word)
    with open('dictionaries/custom/nyt_spelling_bee_dictionary_' + datetime.now().strftime('%Y%m%d'), 'w+') as f:
        f.writelines(word + '\n' for word in updated_word_set if len(word) > 3)


def interactive_edit(solutions: list[str]):
    add_list = []
    delete_list = []

    print("Keep? (y/n)")
    for sol in solutions:
        ip = input(f"{sol} - ")
        if ip == "n":
            delete_list.append(sol)
        else:
            continue

    print("\n Add new words? (y/n)")
    ip = input()
    if ip == "y":
        print("Enter one word per line. Type q to stop.")
        ip = "whatever"
        while ip != "q":
            ip = input()
            if ip != "q":
                add_list.append(ip)

    print("----------------------")
    print(f"Words to be added: {', '.join(add_list)}")
    print(f"Words to be deleted: {', '.join(delete_list)}")
    ip = input("Confirm? (y/n)")
    if ip == "y":
        add_new_words(add_list)
        delete_words(delete_list)


#
# add_new_words(["meme", "memed", "meming", "naan"])
# delete_words(
#     ["gemmed", "gemming", "idem", "legmen", "limed", "liming", "meed", "middled", "aline", "aniline", "ilea", "ilia",
#      "vela", "villae", "viva"])

today_center = "a"
today_others = "eijlnv"
with open(get_latest_custom_dictionary_path()) as reader:
    words = reader.read().splitlines()
nested_dict = preprocess_graph_inception_solution(words, {})
solution_words = get_bee_words_graph_inception(today_center, today_others, nested_dict)
interactive_edit(solution_words)
