from datetime import datetime
from spelling_bee_solvers import get_bee_solutions_radix_tree, _preprocess_get_radix_tree
from dictionary_utils import get_latest_custom_dictionary, write_words_to_dictionary


def add_new_words(new_words: list[str]) -> None:
    """
    Adds words to custom dictionary.
    """
    updated_word_set = set(get_latest_custom_dictionary())
    updated_word_set.update(new_words)
    _write_to_datetime_file(updated_word_set)


def delete_words(delete_list: list[str]):
    """
    Deletes words from custom dictionary.
    """
    updated_word_set = set(get_latest_custom_dictionary())
    for word in delete_list:
        updated_word_set.remove(word)
    _write_to_datetime_file(updated_word_set)


def _write_to_datetime_file(word_list: list[str] | set[str]) -> None:
    write_words_to_dictionary(word_list,
                              f'custom/nyt_spelling_bee_dictionary_{datetime.now().strftime('%Y%m%d')}.txt')


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


today_center = "o"
today_others = "ctpnme"
nested_dict = _preprocess_get_radix_tree(get_latest_custom_dictionary(), {})
solution_words = get_bee_solutions_radix_tree(today_center, today_others, nested_dict)
interactive_edit(solution_words)
