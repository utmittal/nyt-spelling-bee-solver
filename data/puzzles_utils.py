import json
from datetime import date, datetime

from spelling_bee_solvers import validate_character_args
from util.project_path import project_path


class NYTBeePuzzle:
    __center: str
    __others: str
    __solutions: set[str]
    __puzzle_date: date

    def __init__(self, puzzle_data: date, center: str, others: str | list[str] | set[str],
                 solutions: list[str] | set[str]):
        others = ''.join(sorted(others))

        validate_character_args(center, others)

        self.__puzzle_date = puzzle_data
        self.__center = center
        self.__others = others
        self.__solutions = set(solutions.copy())

    def __eq__(self, other):
        if not isinstance(other, NYTBeePuzzle):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (self.__center == other.get_center() and self.__others == other.get_others() and self.__solutions ==
                other.get_solutions() and self.__puzzle_date == other.get_puzzle_date())

    def get_center(self) -> str:
        return self.__center

    def get_others(self) -> str:
        return self.__others

    def get_solutions(self) -> set[str]:
        return self.__solutions.copy()

    def get_puzzle_date(self) -> date:
        return self.__puzzle_date


def write_puzzles_to_file(puzzle_list: list[NYTBeePuzzle]) -> None:
    json_dict = {}
    for puzzle in puzzle_list:
        json_dict[puzzle.get_puzzle_date().strftime('%Y%m%d')] = {'center': puzzle.get_center(),
                                                                  'others': puzzle.get_others(),
                                                                  'solutions': list(puzzle.get_solutions())}
    with open(project_path('data/puzzles/scraped_puzzles.json'), 'w+') as f:
        json.dump(json_dict, f, indent=4, sort_keys=True)


def get_puzzles_from_file() -> dict[date, NYTBeePuzzle]:
    scraped_puzzles_path = project_path('data/puzzles/scraped_puzzles.json')
    if not scraped_puzzles_path.exists():
        return {}

    with open(scraped_puzzles_path, 'r') as f:
        json_dict = json.load(f)

    puzzles: dict[date, NYTBeePuzzle] = dict()
    for date_str, puzzle in json_dict.items():
        puzzle_date = datetime.strptime(date_str, '%Y%m%d').date()
        puzzles[puzzle_date] = NYTBeePuzzle(puzzle_date, puzzle['center'], puzzle['others'],
                                            puzzle['solutions'])

    return puzzles
