"""
This module tests each solver against every puzzle we have in our database to make sure that we are still getting the
correct solution.

This is mostly a safeguard against when I make changes to the solvers. It's sometimes hard to tell you have broken
something because you might be missing only a few of the correct answers.
"""

import pytest

from data.dictionary_utils import get_custom_dictionary
from data.puzzles_utils import get_puzzles_from_file, NYTBeePuzzle
from spelling_bee_solvers import get_bee_solutions_naive, preprocess_get_bit_to_word_dict, get_bee_solutions_bitwise, \
    preprocess_get_prefix_tree, get_bee_solutions_prefix_tree, preprocess_get_nested_prefix_tree, \
    get_bee_solutions_nested_prefix_tree, preprocess_get_radix_tree, get_bee_solutions_radix_tree

PUZZLES = [p[1] for p in sorted(get_puzzles_from_file().items())]
WORDS = get_custom_dictionary()


def puzzle_generator() -> NYTBeePuzzle:
    yield from PUZZLES


def puzzle_id_generator(p: NYTBeePuzzle) -> str:
    return f'{p.get_center()} | {p.get_others()}'


@pytest.mark.parametrize('puzzle', puzzle_generator(), ids=puzzle_id_generator)
def test_get_bee_solutions_naive_returnsAllSolutionsFromOfficialSolutionList(puzzle):
    sols = get_bee_solutions_naive(puzzle.get_center(), puzzle.get_others(), WORDS)

    # our solvers can have more than the valid NYT solutions, but never less
    missing_solutions = puzzle.get_solutions() - set(sols)
    assert len(
        missing_solutions) == 0, (f"Generated solutions did not contain the following words from the official answers "
                                  f"list: {puzzle.get_solutions() - set(sols)}")


@pytest.mark.parametrize('puzzle', puzzle_generator(), ids=puzzle_id_generator)
def test_get_bee_solutions_naive_allReturnedSolutionsAreValid(puzzle):
    sols = get_bee_solutions_naive(puzzle.get_center(), puzzle.get_others(), WORDS)

    invalid_sols = set()
    valid_letters = set(puzzle.get_center() + puzzle.get_others())
    for sol in sols:
        if len(set(sol) - valid_letters) > 0:
            invalid_sols.add(sol)

    assert len(
        invalid_sols) == 0, (f"The following solutions had letters that were not in the set of valid letters ("
                             f"{valid_letters}: {invalid_sols})")


@pytest.fixture(scope='module')
def bit_to_word_dict():
    return preprocess_get_bit_to_word_dict(WORDS)


@pytest.mark.parametrize('puzzle', puzzle_generator(), ids=puzzle_id_generator)
def test_get_bee_solutions_bitwise_returnsAllSolutionsFromOfficialSolutionList(bit_to_word_dict, puzzle):
    sols = get_bee_solutions_bitwise(puzzle.get_center(), puzzle.get_others(), bit_to_word_dict)

    # our solvers can have more than the valid NYT solutions, but never less
    missing_solutions = puzzle.get_solutions() - set(sols)
    assert len(
        missing_solutions) == 0, (f"Generated solutions did not contain the following words from the official answers "
                                  f"list: {puzzle.get_solutions() - set(sols)}")


@pytest.mark.parametrize('puzzle', puzzle_generator(), ids=puzzle_id_generator)
def test_get_bee_solutions_bitwise_allReturnedSolutionsAreValid(bit_to_word_dict, puzzle):
    sols = get_bee_solutions_bitwise(puzzle.get_center(), puzzle.get_others(), bit_to_word_dict)

    invalid_sols = set()
    valid_letters = set(puzzle.get_center() + puzzle.get_others())
    for sol in sols:
        if len(set(sol) - valid_letters) > 0:
            invalid_sols.add(sol)

    assert len(
        invalid_sols) == 0, (f"The following solutions had letters that were not in the set of valid letters ("
                             f"{valid_letters}: {invalid_sols})")


@pytest.fixture(scope='module')
def prefix_tree():
    return preprocess_get_prefix_tree(WORDS)


@pytest.mark.parametrize('puzzle', puzzle_generator(), ids=puzzle_id_generator)
def test_get_bee_solutions_prefix_tree_returnsAllSolutionsFromOfficialSolutionList(prefix_tree, puzzle):
    sols = get_bee_solutions_prefix_tree(puzzle.get_center(), puzzle.get_others(), prefix_tree)

    # our solvers can have more than the valid NYT solutions, but never less
    missing_solutions = puzzle.get_solutions() - set(sols)
    assert len(
        missing_solutions) == 0, (f"Generated solutions did not contain the following words from the official answers "
                                  f"list: {puzzle.get_solutions() - set(sols)}")


@pytest.mark.parametrize('puzzle', puzzle_generator(), ids=puzzle_id_generator)
def test_get_bee_solutions_prefix_tree_allReturnedSolutionsAreValid(prefix_tree, puzzle):
    sols = get_bee_solutions_prefix_tree(puzzle.get_center(), puzzle.get_others(), prefix_tree)

    invalid_sols = set()
    valid_letters = set(puzzle.get_center() + puzzle.get_others())
    for sol in sols:
        if len(set(sol) - valid_letters) > 0:
            invalid_sols.add(sol)

    assert len(
        invalid_sols) == 0, (f"The following solutions had letters that were not in the set of valid letters ("
                             f"{valid_letters}: {invalid_sols})")


@pytest.fixture(scope='module')
def nested_prefix_tree():
    return preprocess_get_nested_prefix_tree('', WORDS, {})


@pytest.mark.parametrize('puzzle', puzzle_generator(), ids=puzzle_id_generator)
def test_get_bee_solutions_nested_prefix_tree_returnsAllSolutionsFromOfficialSolutionList(nested_prefix_tree, puzzle):
    sols = get_bee_solutions_nested_prefix_tree(puzzle.get_center(), puzzle.get_others(), nested_prefix_tree)

    # our solvers can have more than the valid NYT solutions, but never less
    missing_solutions = puzzle.get_solutions() - set(sols)
    assert len(
        missing_solutions) == 0, (f"Generated solutions did not contain the following words from the official answers "
                                  f"list: {puzzle.get_solutions() - set(sols)}")


@pytest.mark.parametrize('puzzle', puzzle_generator(), ids=puzzle_id_generator)
def test_get_bee_solutions_nested_prefix_tree_allReturnedSolutionsAreValid(nested_prefix_tree, puzzle):
    sols = get_bee_solutions_nested_prefix_tree(puzzle.get_center(), puzzle.get_others(), nested_prefix_tree)

    invalid_sols = set()
    valid_letters = set(puzzle.get_center() + puzzle.get_others())
    for sol in sols:
        if len(set(sol) - valid_letters) > 0:
            invalid_sols.add(sol)

    assert len(
        invalid_sols) == 0, (f"The following solutions had letters that were not in the set of valid letters ("
                             f"{valid_letters}: {invalid_sols})")


@pytest.fixture(scope='module')
def radix_tree():
    return preprocess_get_radix_tree(WORDS, {})


@pytest.mark.parametrize('puzzle', puzzle_generator(), ids=puzzle_id_generator)
def test_get_bee_solutions_radix_tree_returnsAllSolutionsFromOfficialSolutionList(radix_tree, puzzle):
    sols = get_bee_solutions_radix_tree(puzzle.get_center(), puzzle.get_others(), radix_tree)

    # our solvers can have more than the valid NYT solutions, but never less
    missing_solutions = puzzle.get_solutions() - set(sols)
    assert len(
        missing_solutions) == 0, (f"Generated solutions did not contain the following words from the official answers "
                                  f"list: {puzzle.get_solutions() - set(sols)}")


@pytest.mark.parametrize('puzzle', puzzle_generator(), ids=puzzle_id_generator)
def test_get_bee_solutions_radix_tree_allReturnedSolutionsAreValid(radix_tree, puzzle):
    sols = get_bee_solutions_radix_tree(puzzle.get_center(), puzzle.get_others(), radix_tree)

    invalid_sols = set()
    valid_letters = set(puzzle.get_center() + puzzle.get_others())
    for sol in sols:
        if len(set(sol) - valid_letters) > 0:
            invalid_sols.add(sol)

    assert len(
        invalid_sols) == 0, (f"The following solutions had letters that were not in the set of valid letters ("
                             f"{valid_letters}: {invalid_sols})")


@pytest.mark.parametrize('puzzle', puzzle_generator(), ids=puzzle_id_generator)
def test_all_solvers_return_the_same_answers(bit_to_word_dict, prefix_tree, nested_prefix_tree, radix_tree, puzzle):
    """
    Tests the unlikely corner case where a change we make means that one solver returns more/less answers than the
    others, while still returning all the correct answers as per the official list.
    """
    naive_sols = set(get_bee_solutions_naive(puzzle.get_center(), puzzle.get_others(), WORDS))
    bitwise_sols = set(get_bee_solutions_bitwise(puzzle.get_center(), puzzle.get_others(), bit_to_word_dict))
    prefix_sols = set(get_bee_solutions_prefix_tree(puzzle.get_center(), puzzle.get_others(), prefix_tree))
    nested_prefix_sols = set(
        get_bee_solutions_nested_prefix_tree(puzzle.get_center(), puzzle.get_others(), nested_prefix_tree))
    radix_sols = set(get_bee_solutions_radix_tree(puzzle.get_center(), puzzle.get_others(), radix_tree))

    # list out separately for nicer error messages
    assert naive_sols == bitwise_sols
    assert naive_sols == prefix_sols
    assert naive_sols == nested_prefix_sols
    assert naive_sols == radix_sols
