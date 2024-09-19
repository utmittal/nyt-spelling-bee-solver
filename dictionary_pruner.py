"""
Experimental code to prune our custom dictionary based on past correct answers from nytbee.com.

To avoid scraping the website again, I am going to try to read the existing file and try to identify the puzzle based
on the answers. And then get answers from our dictionary for that puzzle and add/remove words as required.
"""
from dictionary_utils import PROJECT_ROOT_PATH, get_latest_custom_dictionary
from interactive_editor import add_new_words, delete_words
from spelling_bee_solvers import preprocess_get_radix_tree, get_bee_solutions_radix_tree

radix_tree = preprocess_get_radix_tree(get_latest_custom_dictionary(), {})


def _get_bee_sols(cen: str, oth: list[str]) -> list[str]:
    return get_bee_solutions_radix_tree(cen, ''.join(oth), radix_tree)


with open(f'{PROJECT_ROOT_PATH}/dictionaries/raw/nytbee_dot_com_scraped_answers.txt', 'r') as reader:
    nyt_bee_answers = reader.read().splitlines()

current_letters = set()
current_words = set()
probable_center = set()
total_add = set()
total_delete = set()
for word in nyt_bee_answers:
    letter_set = set(word)

    if len(current_letters.union(letter_set)) > 7:
        if len(current_letters) == 7:
            if len(probable_center) != 1:
                # Add all words but don't delete anything
                total_add.update(current_words)
                print(f"Could not find center for letter set: {current_letters}.")
                current_letters = set()
                current_words = set()
                probable_center = set()
                continue

            center = probable_center.pop()
            current_letters.remove(center)
            our_answers = set(_get_bee_sols(center, list(current_letters)))

            words_to_delete = our_answers - current_words
            total_delete.update(words_to_delete)
            words_to_add = current_words - our_answers
            total_add.update(words_to_add)
            # print(f"center: {center}")
            # print(f"others: {current_letters}")
            # print(f"nyt bee words: {current_words}")
            # print(f"our answers: {our_answers}")
            # print(f"delete: {words_to_delete}")
            # print(f"add: {words_to_add}")

            current_letters = set()
            current_words = set()
            probable_center = set()
        else:
            raise Exception(
                "Current word seems to start a new puzzle but we haven't found all the letters in the old puzzle yet.")
    else:
        current_letters.update(letter_set)
        if len(probable_center) == 0:
            probable_center.update(letter_set)
        else:
            probable_center.intersection_update(letter_set)
        current_words.add(word)

print(total_add)
print(total_delete)

add_new_words(list(total_add))
delete_words(list(total_delete))
