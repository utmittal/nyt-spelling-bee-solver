from datetime import datetime, timedelta
from urllib.error import HTTPError

from scraper.nyt_bee_scraper import _get_date_string, get_url_from_date, get_raw_page, add_date_and_url_to_file, \
    get_answer_list_from_nyt_page, add_words_to_raw_scraped_dictionary
from util.project_path import project_path

date_object = datetime.now()
unique_words_aim = 10237

with open(project_path('scraper/logs/scraped_dates.txt'), 'r') as f:
    already_scraped = f.read().splitlines()
scraped_dates = [w.split(',')[0] for w in already_scraped]

with open(project_path('dictionaries/raw/nytbee_dot_com_scraped_answers.txt'), 'r') as f:
    unique_words = set(f.read().splitlines())

consecutive_404 = False
while True:
    date_object = date_object - timedelta(days=1)
    date_string = _get_date_string(date_object)
    if date_string in scraped_dates:
        consecutive_404 = False
        continue

    current_url = get_url_from_date(date_object)

    print("Processing - " + current_url)
    try:
        raw_page = get_raw_page(current_url)
    except HTTPError as e:
        if e.code == 404 and consecutive_404 == False:
            add_date_and_url_to_file('logs/known_missing_pages.txt', date_object)
            print("Page doesn't exist. Continuing.")
            consecutive_404 = True
            continue
        else:
            raise e

    consecutive_404 = False

    answer_list = get_answer_list_from_nyt_page(raw_page)
    print("Found " + str(len(answer_list)) + " words.")

    # Note: we don't dedupe the answers before writing. We just want all the answers.
    add_words_to_raw_scraped_dictionary(answer_list)
    unique_words.update(answer_list)
    print("Unique word count - " + str(len(unique_words)))

    if len(unique_words) == unique_words_aim:
        print("Found all unique words. Terminating scraping.")

    add_date_and_url_to_file('logs/scraped_dates.txt', date_object)
