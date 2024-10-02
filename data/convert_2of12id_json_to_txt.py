import json

from util.project_path import project_path


def _convert_categorized_json_to_wordlist_file() -> None:
    with open(project_path('data/raw_word_lists/2of12id.json'), 'r') as f:
        json_words = json.load(f)
    word_list = []
    for key in json_words:
        word_list.extend(json_words[key])

    with open(project_path('data/processed/words_2of12id.txt'), 'w+') as writefile:
        writefile.writelines(word.lower() + '\n' for word in sorted(word_list))


_convert_categorized_json_to_wordlist_file()
