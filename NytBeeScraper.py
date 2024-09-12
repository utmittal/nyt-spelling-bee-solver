from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import backoff


def fatal_code(excep):
    if excep.code == 404:
        return True
    else:
        return False


@backoff.on_exception(backoff.expo,
                      HTTPError,
                      max_tries=10,
                      giveup=fatal_code)
def get_raw_page(url):
    req = Request(url)

    user_agent_header = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    req.add_header('user-agent', user_agent_header)

    return urlopen(req).read()


def get_answers_list_from_answers_div(answers_div):
    # all_text can contain answers and ↗ (the symbol for the definition link on the nytbee page), so we need to filter
    # it
    all_text = answers_div.get_text(strip=True, separator=',')
    answers = [w for w in all_text.split(sep=',') if w.isalpha()]
    if len(answers) == 0:
        raise LookupError("Found answer list of length 0.")

    return answers


def answers_from_main_answer_list(soup):
    """
    This seems to work from 2019 08 17 onwards
    """
    # The list of answers seems to always be in a div with id=main-answer-list
    answer_list_div = soup.find(id="main-answer-list")
    if answer_list_div is None:
        raise LookupError("Could not find element with id=main-answer-list.")

    return get_answers_list_from_answers_div(answer_list_div)


def answers_from_top_container(soup):
    """
    2019 08 16 and before
    """
    # There are multiple divs with class answer-list so we first find top-container
    top_container_div = soup.find(id="top-container")
    if top_container_div is None:
        raise LookupError("Could not find element with id=top-container.")
    answer_list_div = top_container_div.find(class_="answer-list")
    if answer_list_div is None:
        raise LookupError("Could not find element with class=answer-list")

    return get_answers_list_from_answers_div(answer_list_div)


def get_answer_list_from_nyt_page(raw_web_page):
    soup = BeautifulSoup(raw_web_page, "html.parser")

    try:
        answers = answers_from_main_answer_list(soup)
    except LookupError:
        answers = answers_from_top_container(soup)

    # Verify our answer list
    pattern = r"Number of Answers: (\d+)"
    number_of_answers = re.search(pattern, raw_web_page.decode('utf-8'))
    groups = number_of_answers.groups()
    if len(groups) > 1:
        raise LookupError("Found more than one match for number of answers.")
    else:
        web_page_answers_count = int(groups[0])
        if web_page_answers_count != len(answers):
            raise LookupError("Number of answers as per page is " + str(
                web_page_answers_count) + " but the scraper only found " + str(len(answers)) + " answers.")

    return answers


def write_words_to_dictionary(word_list):
    # Note: we specifically open in append mode so that if for some reason the file doesn't exist, the program fails.
    # I want to know if the file is gone (because something has gone wrong)
    with open('dictionary/nytbee_dot_com_scraped_answers.txt', 'a') as writefile:
        writefile.writelines(word + '\n' for word in word_list)


def get_date_string(date):
    return date.strftime('%Y%m%d')


def get_url_from_date(date):
    return "https://nytbee.com/Bee_" + get_date_string(date) + ".html"


def add_date_and_url_to_file(path, date):
    with open(path, 'a+') as thefile:
        thefile.write(get_date_string(date) + ", " + get_url_from_date(date) + "\n")


# datetime(year=2024,month=9,day=12)
date_object = datetime.now()
unique_words_aim = 10237

with open('scraper_logs/scraped_dates.txt', 'r') as f:
    already_scraped = f.read().splitlines()
scraped_dates = [w.split(',')[0] for w in already_scraped]

with open('dictionary/nytbee_dot_com_scraped_answers.txt', 'r') as f:
    unique_words = set(f.read().splitlines())

consecutive_404 = False
while True:
    date_object = date_object - timedelta(days=1)
    date_string = get_date_string(date_object)
    if date_string in scraped_dates:
        consecutive_404 = False
        continue

    current_url = get_url_from_date(date_object)

    print("Processing - " + current_url)
    try:
        raw_page = get_raw_page(current_url)
    except HTTPError as e:
        if e.code == 404 and consecutive_404 == False:
            add_date_and_url_to_file('scraper_logs/missing_pages.txt', date_object)
            print("Page doesn't exist. Continuing.")
            consecutive_404 = True
            continue
        else:
            raise e

    consecutive_404 = False

    answer_list = get_answer_list_from_nyt_page(raw_page)
    print("Found " + str(len(answer_list)) + " words.")

    # Note: we don't dedupe the answers before writing. We just want all the answers.
    write_words_to_dictionary(answer_list)
    unique_words.update(answer_list)
    print("Unique word count - " + str(len(unique_words)))

    if len(unique_words) == unique_words_aim:
        print("Found all unique words. Terminating scraping.")

    add_date_and_url_to_file('scraper_logs/scraped_dates.txt', date_object)
