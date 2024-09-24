from datetime import datetime, timedelta
from urllib.error import HTTPError

from dictionaries.dictionary_utils import get_dictionary_from_path, write_words_to_dictionary
from scraper.nyt_bee_scraper import get_date_string, get_url_from_date, get_raw_page, add_date_and_url_to_file, \
    get_answer_list_from_nyt_page, add_words_to_raw_scraped_dictionary, get_url_date_dict_from_logfile, \
    write_url_date_dict_to_logfile

date_object = datetime.now()
unique_words_aim = 10237

scraped_urls = get_url_date_dict_from_logfile('scraper/logs/scraped_dates.txt')
known_missing_urls = get_url_date_dict_from_logfile('scraper/logs/known_missing_pages.txt')
unique_words = get_dictionary_from_path('dictionaries/raw/nytbee_dot_com_scraped_answers.txt')

try:
    consecutive_404 = False
    while True:
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

        # Note: we don't dedupe the answers before writing. We just want all the answers.
        unique_words.extend(answer_list)
        print("Unique word count - " + str(len(unique_words)))

        if len(unique_words) >= unique_words_aim:
            print("Found all unique words. Terminating scraping.")
            break

        scraped_urls[current_url] = get_date_string(date_object)
finally:
    write_words_to_dictionary(unique_words, 'dictionaries/raw/nytbee_dot_com_scraped_answers.txt')
    write_url_date_dict_to_logfile(scraped_urls, 'scraper/logs/scraped_dates.txt')
    write_url_date_dict_to_logfile(known_missing_urls, 'scraper/logs/known_missing_pages.txt')
