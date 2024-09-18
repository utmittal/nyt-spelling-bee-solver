import argparse

from dictionary_utils import get_latest_custom_dictionary
from spelling_bee_solvers import _preprocess_get_radix_tree, get_bee_solutions_radix_tree

parser = argparse.ArgumentParser(
    description="Generates a list of solutions for the NYT Spelling Bee.",
    epilog="Note: The list of solutions may contain extra words or be missing some words. NYT doesn't publish a set "
           "dictionary for the Spelling Bee so this script uses a custom dictionary which may not be completely "
           "accurate.",
    add_help=True)
parser.add_argument("-c", "--center", required=True, nargs=1, dest="center", metavar="letter",
                    help="Central letter that must be used in the solutions (1 letter).")
parser.add_argument("-o", "--others", required=True, nargs=1, dest="others", metavar="letters",
                    help="Other letters that must be used in the solutions (6 letters).")
args = parser.parse_args()
# nargs returns a list
center = args.center[0]
others = args.others[0]

with open(get_latest_custom_dictionary()) as dictionary_reader:
    words = dictionary_reader.read().splitlines()

radix_tree = _preprocess_get_radix_tree(words, {})
solutions = get_bee_solutions_radix_tree(center, others, radix_tree)

print(f"Spelling Bee Solutions - [{center.upper()} | {' '.join(c.upper() for c in others)}]:")
for sol in sorted(solutions):
    print(f"    {sol}")
