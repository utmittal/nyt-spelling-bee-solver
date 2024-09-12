from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import backoff

@backoff.on_exception(backoff.expo,
                      HTTPError,
                      max_tries=5)
def get_raw_page(url):
    req = Request(url)

    user_agent_header = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    req.add_header('user-agent',user_agent_header)

    return urlopen(req).read()

def get_answer_list_from_nyt_page(raw_web_page):
    soup = BeautifulSoup(raw_web_page, "html.parser")

    # The list of answers seems to always be in a div with id=main-answer-list
    answer_list_div = soup.find(id="main-answer-list")
    if answer_list_div is None:
        raise LookupError("Could not find element with id=main-answer-list.")

    # all_text should contain answers and ↗ (the symbol for the definition link on the nytbee page)
    all_text = answer_list_div.get_text(strip=True, separator=',')
    answers = [w for w in all_text.split(sep=',') if w.isalpha()]
    if len(answers) == 0:
        raise LookupError("Found answer list of length 0.")

    # Verify our answer list
    pattern = r"Number of Answers: (\d+)"
    number_of_answers = re.search(pattern,raw_web_page.decode('utf-8'))
    groups = number_of_answers.groups()
    if len(groups) > 1:
        raise LookupError("Found more than one match for number of answers.")
    else:
        web_page_answers_count = int(groups[0])
        if web_page_answers_count != len(answers):
            raise LookupError("Number of answers as per page is " + str(web_page_answers_count) + " but the scraper only found " + str(len(answers)) + " answers.")

    return answers

def write_words_to_dictionary(word_list):
    # Note: we specifically open in append mode so that if for some reason the file doesn't exist, the program fails.
    # I want to know if the file is gone (because something has gone wrong)
    with open('dictionary/nytbee_dot_com_scraped_answers.txt','a') as writefile:
        writefile.writelines(word + '\n' for word in word_list)

# datetime(year=2024,month=9,day=12)
date_object = datetime.now()
with open('scraper_logs/scraped_dates.txt','r') as f:
    already_scraped = f.read().splitlines()
scraped_dates = [w.split(',')[0] for w in already_scraped]
while True:
    date_object = date_object - timedelta(days=1)
    date_string = date_object.strftime('%Y%m%d')
    if date_string in scraped_dates:
        continue

    current_url = "https://nytbee.com/Bee_"+date_string+".html"

    print("Processing - " + current_url)
    raw_page = get_raw_page(current_url)
    answer_list = get_answer_list_from_nyt_page(raw_page)
    print("Found " + str(len(answer_list)) + " words.")

    # Note: we don't dedupe the answers before writing. We just want all the answers.
    write_words_to_dictionary(answer_list)

    with open('scraper_logs/scraped_dates.txt','a+') as afile:
        afile.write(date_string + ", " + current_url + "\n")