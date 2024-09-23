from spelling_bee_solvers import get_bee_solutions_radix_tree, preprocess_get_radix_tree
from dictionaries.dictionary_utils import get_latest_custom_dictionary, write_words_to_custom_dictionary


def add_new_words(new_words: list[str]) -> None:
    """
    Adds words to custom dictionary.
    """
    updated_word_set = set(get_latest_custom_dictionary())
    updated_word_set.update(new_words)
    write_words_to_custom_dictionary(updated_word_set)


def delete_words(delete_list: list[str]):
    """
    Deletes words from custom dictionary.
    """
    updated_word_set = set(get_latest_custom_dictionary())
    for word in delete_list:
        updated_word_set.remove(word)
    write_words_to_custom_dictionary(updated_word_set)


def interactive_edit(solutions: list[str]) -> None:
    solutions = sorted(solutions)
    add_list = []
    delete_list = []

    print("Keep? (y/n)")
    for sol in solutions:
        ip = input(f"{sol} - ")
        if ip == "n":
            delete_list.append(sol)
        elif len(ip) > 1:
            add_list.append(ip)
        else:
            continue

    print("----------------------")
    print(f"Words to be added: {', '.join(add_list)}")
    print(f"Words to be deleted: {', '.join(delete_list)}")
    ip = input("Confirm? (y/n)")
    if ip == "y":
        add_new_words(add_list)
        delete_words(delete_list)


today_center = "y"
today_others = "adeilz"
nested_dict = preprocess_get_radix_tree(get_latest_custom_dictionary(), {})
solution_words = get_bee_solutions_radix_tree(today_center, today_others, nested_dict)
interactive_edit(solution_words)
