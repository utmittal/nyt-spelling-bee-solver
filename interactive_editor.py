from dictionaries.dictionary_utils import (get_latest_custom_dictionary, write_words_to_custom_dictionary,
                                           add_new_words, \
    delete_words)
from spelling_bee_solvers import get_bee_solutions_radix_tree, preprocess_get_radix_tree


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
