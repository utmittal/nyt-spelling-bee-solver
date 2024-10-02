from data.dictionary_utils import get_dictionary_from_path, write_words_to_dictionary

words_alpha_list = get_dictionary_from_path('data/raw_word_lists/words_alpha.txt')
write_words_to_dictionary(words_alpha_list, 'data/processed/filtered_words_alpha.txt')

words_alpha_list = get_dictionary_from_path('data/processed/words_2of12id.txt')
write_words_to_dictionary(words_alpha_list, 'data/processed/filtered_words_2of12id.txt')
