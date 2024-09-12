from urllib.request import urlopen, Request

from bs4 import BeautifulSoup

url = "https://nytbee.com/Bee_20240911.html"
req = Request(url)
req.add_header('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
rawpage = urlopen(req).read()

soup = BeautifulSoup(rawpage, "html.parser")
answer_list = soup.find(id="main-answer-list")

print(answer_list.get_text(strip=True,separator=','))