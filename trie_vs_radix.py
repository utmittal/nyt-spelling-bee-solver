import time

from dictionaries.dictionary_utils import get_benchmarking_dictionary
from spelling_bee_solvers import preprocess_get_prefix_tree, \
    preprocess_get_radix_tree, get_bee_solutions_prefix_tree, \
    get_bee_solutions_radix_tree, prefix_max_depth, prefix_leaf_nodes_touched, prefix_aborted_early, radix_max_depth, \
    radix_leaf_nodes_touched, radix_aborted_early, prefix_find_next_chars, prefix_abort_early_time, prefix_add_words, \
    radix_add_words

# NYT Spelling Bee Puzzle from 2019/06/08 which had the most official solutions
benchmark_center = 'o'
benchmark_others = 'ctpnme'
benchmarking_word_list = get_benchmarking_dictionary()

prefix_tree = preprocess_get_prefix_tree('', benchmarking_word_list, {})
radix_tree = preprocess_get_radix_tree(benchmarking_word_list, {})

start = time.time()
for _ in range(100):
    get_bee_solutions_prefix_tree(benchmark_center, benchmark_others, prefix_tree)
end = time.time()
print(f"Prefix tree total time: {end - start}")
print(
    f"\tMax depth: {prefix_max_depth}\n\tLeaf nodes touched: {prefix_leaf_nodes_touched}\n\tAborted early: "
    f"{prefix_aborted_early}\n\tNext char time: {prefix_find_next_chars}\n\tAbort early time: "
    f"{prefix_abort_early_time}\n\tAdd words time: {prefix_add_words}")

start = time.time()
for _ in range(100):
    get_bee_solutions_radix_tree(benchmark_center, benchmark_others, radix_tree)
end = time.time()
print(f"Radix tree total time: {end - start}")
print(
    f"\tMax depth: {radix_max_depth}\n\tLeaf nodes touched: {radix_leaf_nodes_touched}\n\tAborted early: "
    f"{radix_aborted_early}\n\tAdd words time: {radix_add_words}")

small_dict = ["rot", "rob", "rat"]

small_prefix_dict = preprocess_get_prefix_tree('', small_dict, {})
print(small_prefix_dict)
small_radix_dict = preprocess_get_radix_tree(small_dict, {})
print(small_radix_dict)
