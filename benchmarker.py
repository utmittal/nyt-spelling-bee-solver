import timeit

from tabulate import tabulate

from dictionaries.dictionary_utils import get_benchmarking_dictionary
# noinspection PyUnresolvedReferences
from spelling_bee_solvers import preprocess_get_bit_to_word_dict, preprocess_get_prefix_tree, \
    preprocess_get_radix_tree, get_bee_solutions_naive, get_bee_solutions_bitwise, get_bee_solutions_prefix_tree, \
    get_bee_solutions_radix_tree

# NYT Spelling Bee Puzzle from 2019/06/08 which had the most official solutions
benchmark_center = 'o'
benchmark_others = 'ctpnme'
benchmarking_word_list = get_benchmarking_dictionary()

bit_to_word_dict = preprocess_get_bit_to_word_dict(benchmarking_word_list)
prefix_tree = preprocess_get_prefix_tree(benchmarking_word_list)
radix_tree = preprocess_get_radix_tree(benchmarking_word_list, {})

naive_solution_stmt = """
get_bee_solutions_naive(benchmark_center, benchmark_others, benchmarking_word_list)
"""

bitwise_solution_stmt = """
get_bee_solutions_bitwise(benchmark_center, benchmark_others, bit_to_word_dict)
"""

prefix_tree_solution_stmt = """
get_bee_solutions_prefix_tree(benchmark_center, benchmark_others, prefix_tree)
"""

radix_tree_solution_stmt = """
get_bee_solutions_radix_tree(benchmark_center, benchmark_others, radix_tree)
"""

iterations = 10000
repetitions = 5  # default

naive_results = timeit.repeat(stmt=naive_solution_stmt, number=iterations, repeat=repetitions, globals=globals())
naive_min = min([r / iterations for r in naive_results])

bitwise_results = timeit.repeat(stmt=bitwise_solution_stmt, number=iterations, repeat=repetitions, globals=globals())
bitwise_min = min([r / iterations for r in bitwise_results])

prefix_tree_results = timeit.repeat(stmt=prefix_tree_solution_stmt, number=iterations, repeat=repetitions,
                                    globals=globals())
prefix_tree_min = min([r / iterations for r in prefix_tree_results])

radix_tree_results = timeit.repeat(stmt=radix_tree_solution_stmt, number=iterations, repeat=repetitions,
                                   globals=globals())
radix_tree_min = min([r / iterations for r in radix_tree_results])

print(f"Iterations:\t\t{iterations}")
print(f"Repetitions:\t{repetitions}")
print()
print(tabulate([['Naive', naive_min, naive_min / naive_min], ['Bitwise', bitwise_min, naive_min / bitwise_min],
                ['Prefix Tree', prefix_tree_min, naive_min / prefix_tree_min],
                ['Radix Tree', radix_tree_min, naive_min / radix_tree_min]],
               headers=['Strategy', 'Min Time (s)', 'Speedup']))

"""
Iterations:		10000
Repetitions:	5

Strategy       Min Time (s)    Speedup
-----------  --------------  ---------
Naive           0.0578143      1
Bitwise         0.0132765      4.35462
Prefix Tree     0.000579531   99.7605
Radix Tree      0.000454482  127.209
"""
