### words_2of12id.txt

`.txt` version of `/data/raw_word_lists/2of12id.json` which removes all category information and adds one word per line.

### filtered_words_2of12id.txt

Filtered version of `words_2of12id.txt` that removes all words that cannot be played in NYT Spelling Bee. This includes
words of length less than 4 character or words of length more than 19 character or words with more than 7 unique
letters.

### filtered_words_alpha.txt

Filtered version of `/data/raw_word_lists/words_alpha.txt` that removes all words that cannot be played in NYT Spelling
Bee. This includes words of length less than 4 character or words of length more than 19 character or words with more
than 7 unique letters.

### nytbee_dot_com_scraped_answers.txt

List of all official answers as per the unofficial website nytbee.com. This list is updated semi-regularly.