"""
Simple web scraping script to download all correct answers from unscraped pages and update our dictionary.
"""
from datetime import datetime, timedelta
from urllib.error import HTTPError

from dictionaries.dictionary_utils import get_dictionary_from_path, write_words_to_dictionary, \
    get_latest_custom_dictionary, add_new_words, delete_words
from scraper.nyt_bee_scraper import get_date_string, get_url_from_date, get_raw_page, \
    get_answer_list_from_nyt_page, get_url_date_dict_from_logfile, \
    write_url_date_dict_to_logfile, get_max_unique_words, get_non_official_answers_from_nyt_page
from spelling_bee_solvers import preprocess_get_radix_tree, get_bee_solutions_radix_tree

date_object = datetime.now()
starting_date = date_object - timedelta(days=1)
unique_words_aim = get_max_unique_words(get_url_from_date(starting_date))
print(f"Max unique word count = {unique_words_aim} from {get_url_from_date(starting_date)}")

scraped_urls = get_url_date_dict_from_logfile('scraper/logs/scraped_dates.txt')
known_missing_urls = get_url_date_dict_from_logfile('scraper/logs/known_missing_pages.txt')
undetermined_center_urls = get_url_date_dict_from_logfile('scraper/logs/undetermined_center_pages.txt')
unique_words = set(get_dictionary_from_path('dictionaries/raw/nytbee_dot_com_scraped_answers.txt'))

radix_tree = preprocess_get_radix_tree(get_latest_custom_dictionary(), {})

words_to_add = set()
words_to_delete = set()
try:
    consecutive_404 = False
    while date_object > datetime(year=2018, month=7, day=28):  # oldest nytbee.com page
        date_object = date_object - timedelta(days=1)

        current_url = get_url_from_date(date_object)
        if current_url in scraped_urls or current_url in known_missing_urls:
            consecutive_404 = False
            continue

        print("Processing - " + current_url)
        try:
            raw_page = get_raw_page(current_url)
        except HTTPError as e:
            if e.code == 404 and consecutive_404 == False:
                known_missing_urls[current_url] = get_date_string(date_object)
                print("Page doesn't exist. Continuing.")
                consecutive_404 = True
                continue
            else:
                raise e

        consecutive_404 = False

        answer_list = get_answer_list_from_nyt_page(raw_page)
        print("Found " + str(len(answer_list)) + " words.")

        # Only used for determining the puzzle for today.
        non_official_answers = []
        # nytbee.com didn't publish non-official words before this date.
        if date_object > datetime(year=2019, month=11, day=13):
            non_official_answers = get_non_official_answers_from_nyt_page(raw_page)
            print(f"Found {str(len(non_official_answers))} non-official words.")

        todays_letter_set = set()
        todays_center = set()
        for word in answer_list + non_official_answers:
            letters = set(word)
            todays_letter_set.update(letters)
            if todays_center == set():
                todays_center.update(letters)
            else:
                todays_center.intersection_update(letters)
        if len(todays_letter_set) > 7:
            raise Exception("Found more than 7 letters based on answer list. Wtf?")
        elif len(todays_center) > 1:
            print(f"Could not determine center letter. Current candidates: {todays_center}")
            undetermined_center_urls[current_url] = get_date_string(date_object)
        elif len(todays_center) < 1:
            raise Exception("Found no center letter based on answer list. Wtf?")
        else:
            other_letters = todays_letter_set - todays_center
            center_letter = todays_center.pop()

            solutions = set(get_bee_solutions_radix_tree(center_letter, ''.join(other_letters), radix_tree))
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

        # Note: we don't dedupe the answers before writing. We just want all the answers.
        unique_words.update(answer_list)
        print("Unique word count - " + str(len(unique_words)))

        scraped_urls[current_url] = get_date_string(date_object)
finally:
    try:
        write_words_to_dictionary(unique_words, 'dictionaries/raw/nytbee_dot_com_scraped_answers.txt')
        write_url_date_dict_to_logfile(scraped_urls, 'scraper/logs/scraped_dates.txt')
        write_url_date_dict_to_logfile(known_missing_urls, 'scraper/logs/known_missing_pages.txt')
        write_url_date_dict_to_logfile(undetermined_center_urls, 'scraper/logs/undetermined_center_pages.txt')
        add_new_words(words_to_add)
        delete_words(words_to_delete)
    except Exception:
        print('-------------------------')
        print(
            f"Unique Words: {unique_words}\nScraped URLs: {scraped_urls}\nKnown Missing URLs: "
            f"{known_missing_urls}\nUndetermined center URLs: {undetermined_center_urls}\nWords to add: "
            f"{words_to_add}\nWords to delete: {words_to_delete}")
