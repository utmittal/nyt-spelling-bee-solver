"""
Simple web scraping script to download all known correct answers from nytbee.com.
"""
import re
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen, Request

import backoff
from bs4 import BeautifulSoup, NavigableString, Tag

from util.project_path import project_path


def _fatal_code(excep: Exception):
    if isinstance(excep, HTTPError) and excep.code == 404:
        return True
    else:
        return False


@backoff.on_exception(backoff.expo,
                      HTTPError,
                      max_tries=10,
                      giveup=_fatal_code)
def get_raw_page(url: str) -> bytes:
    req = Request(url)

    user_agent_header = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/103.0.0.0 Safari/537.36')
    req.add_header('user-agent', user_agent_header)

    return urlopen(req).read()


def _get_answers_list_from_answers_div(answers_div: BeautifulSoup | Tag | NavigableString) -> list[str]:
    # all_text can contain answers and ↗ (the symbol for the definition link on the nytbee page), so we need to filter
    # it
    all_text = answers_div.get_text(strip=True, separator=',')
    answers = [w for w in all_text.split(sep=',') if w.isalpha()]
    if len(answers) == 0:
        raise LookupError("Found answer list of length 0.")

    return answers


def _answers_from_main_answer_list(soup: BeautifulSoup) -> list[str]:
    """
    This seems to work from 2019 08 17 onwards
    """
    # The list of answers seems to always be in a div with id=main-answer-list
    answer_list_div = soup.find(id="main-answer-list")
    if answer_list_div is None:
        raise LookupError("Could not find element with id=main-answer-list.")

    return _get_answers_list_from_answers_div(answer_list_div)


def _answers_from_top_container(soup: BeautifulSoup) -> list[str]:
    """
    2019 08 16 and before
    """
    # There are multiple divs with class answer-list so we first find top-container
    top_container_div = soup.find(id="top-container")
    if top_container_div is None:
        raise LookupError("Could not find element with id=top-container.")
    answer_list_div = top_container_div.find(class_="answer-list")
    if answer_list_div is None:
        # this happens 2018 07 30 and before
        answer_list_div = top_container_div.find(id="answer-list")
        if answer_list_div is None:
            raise LookupError("Could not find element with class or id=answer-list.")

    return _get_answers_list_from_answers_div(answer_list_div)


def _answers_from_left_container(soup: BeautifulSoup) -> list[str]:
    """
    2018 07 29 and before
    """
    # There are multiple divs with class answer-list so we first find top-container
    top_container_div = soup.find(class_="left-container")
    if top_container_div is None:
        raise LookupError("Could not find element with id=top-container.")
    answer_list_div = top_container_div.find(id="answer-list")
    if answer_list_div is None:
        raise LookupError("Could not find element with id=answer-list.")

    return _get_answers_list_from_answers_div(answer_list_div)


def get_answer_list_from_nyt_page(raw_web_page) -> list[str]:
    soup = BeautifulSoup(raw_web_page, "html.parser")

    # try strategies in order
    strategies = [_answers_from_main_answer_list, _answers_from_top_container, _answers_from_left_container]
    answers = []
    for strat in strategies:
        try:
            answers = strat(soup)
        except LookupError:
            continue
    if len(answers) == 0:
        raise LookupError("Could not find answers list using any of the current strategies.")

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


def get_date_string(date: datetime) -> str:
    return date.strftime('%Y%m%d')


def get_url_from_date(date: datetime) -> str:
    return "https://nytbee.com/Bee_" + get_date_string(date) + ".html"


def get_url_date_dict_from_logfile(path: str | Path) -> dict[str, str]:
    with open(project_path(path), 'r') as f:
        lines = f.read().splitlines()

    url_date = {}
    for line in lines:
        date, url = line.split(',')
        # Why reverse for the dictionary? Because it makes checking easier and I can't be bothered rewriting the logs
        # to be url,date
        url_date[url.strip()] = date.strip()

    return url_date


def write_url_date_dict_to_logfile(url_date: dict[str, str], path: str | Path) -> None:
    with open(project_path(path), 'w') as writefile:
        for url in sorted(url_date, key=url_date.get, reverse=True):
            writefile.write(f"{url_date[url].strip()}, {url.strip()}\n")
