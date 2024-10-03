from datetime import datetime

from data.dictionary_utils import get_custom_dictionary, get_dictionary_from_path, \
    write_words_to_dictionary, add_words_to_custom, delete_words_from_custom
from data.puzzles_utils import get_puzzles_from_file, write_puzzles_to_file, NYTBeePuzzle
from scraper.nyt_bee_scraper import get_url_date_dict_from_logfile, get_url_from_date, get_raw_page, \
    get_answer_list_from_nyt_page, write_url_date_dict_to_logfile
from spelling_bee_solvers import get_bee_solutions_radix_tree, preprocess_get_radix_tree

scraped_urls = get_url_date_dict_from_logfile('scraper/logs/scraped_dates.txt')
undetermined_center_urls = get_url_date_dict_from_logfile('scraper/logs/undetermined_center_pages.txt')
unique_words = set(get_dictionary_from_path('data/processed/nytbee_dot_com_scraped_answers.txt'))
scraped_puzzles = get_puzzles_from_file()

radix_tree = preprocess_get_radix_tree(get_custom_dictionary(), {})

words_to_add = set()
words_to_delete = set()
determined_urls = set()
for current_url in undetermined_center_urls:
    print("Processing - " + current_url)
    raw_page = get_raw_page(current_url)
    date_object = datetime.strptime(undetermined_center_urls[current_url], '%Y%m%d').date()

    answer_list = get_answer_list_from_nyt_page(raw_page)
    print("Found " + str(len(answer_list)) + " words.")

    todays_letter_set = set()
    for word in answer_list:
        letters = set(word)
        todays_letter_set.update(letters)

    if len(todays_letter_set) != 7:
        raise Exception("Found more or less than 7 letters based on answer list. Wtf?")
    else:
        user_entered_center = input("Enter center letter: ")
        if len(user_entered_center) > 1:
            raise Exception("Center letter should be single character.")

        todays_letter_set.remove(user_entered_center)

        solutions = set(get_bee_solutions_radix_tree(user_entered_center, ''.join(todays_letter_set), radix_tree))
        print(f"Our solver found {len(solutions)} words.")

        extra_words = solutions - set(answer_list) - words_to_delete
        print(f"\t{extra_words} to be deleted.")
        filtered_extra_words = []
        # Handle the corner case that NYT started accepting words later that it didn't accept before. Since we
        # are going in descending order, this means that those words should be in our unique_words list. If they
        # exist there, do not delete them.
        for w in extra_words:
            if w not in unique_words:
                filtered_extra_words.append(w)
        words_to_delete.update(filtered_extra_words)
        if len(extra_words) > len(filtered_extra_words):
            print(f"\t\tOnly {filtered_extra_words} will be deleted.")

        new_words = set(answer_list) - solutions - words_to_add
        print(f"\t{new_words} to be added.")
        words_to_add.update(new_words)

        scraped_puzzles[date_object] = NYTBeePuzzle(date_object, user_entered_center, todays_letter_set, answer_list)

    unique_words.update(answer_list)

    determined_urls.add(current_url)

for url in determined_urls:
    scraped_urls[url] = undetermined_center_urls[url]
    undetermined_center_urls.pop(url)

write_url_date_dict_to_logfile(undetermined_center_urls, 'scraper/logs/undetermined_center_pages.txt')
write_words_to_dictionary(unique_words, 'data/processed/nytbee_dot_com_scraped_answers.txt')
write_puzzles_to_file([scraped_puzzles[p] for p in scraped_puzzles])
write_url_date_dict_to_logfile(scraped_urls, 'scraper/logs/scraped_dates.txt')
add_words_to_custom(words_to_add)
delete_words_from_custom(words_to_delete)
