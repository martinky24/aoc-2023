from dataclasses import dataclass
from pathlib import Path
from pprint import pprint

DAY = 6
INPUT_FILE = Path(f"day{DAY}/input.txt")


@dataclass
class RaceInfo:
    time: int
    distance: int


def load_file(fname: Path) -> list[str]:
    with open(fname) as f:
        return [x.strip() for x in f.readlines()]


def parse_lines(lines: list[str]) -> list[RaceInfo]:
    times = lines[0]
    distances = lines[1]
    times = times.split(":")[1].strip()
    distances = distances.split(":")[1].strip()
    times = [int(x) for x in times.split(" ") if x != ""]
    distances = [int(x) for x in distances.split(" ") if x != ""]
    races = []
    for x, y in zip(times, distances):
        races.append(RaceInfo(time=x, distance=y))
    return races


def calculate_distance(hold_time: int, race_length: int) -> int:
    return (race_length - hold_time) * hold_time


def calc_wins(race_info: RaceInfo) -> int:
    counter = 0
    for i in range(race_info.time):
        distance = calculate_distance(i, race_info.time)
        if distance > race_info.distance:
            counter += 1
    return counter


if __name__ == "__main__":
    lines = """
Time:      7  15   30
Distance:  9  40  200""".split("\n")[1:]
    lines = load_file(INPUT_FILE)

    races = parse_lines(lines)
    pprint(races)

    product = 1
    for race in races:
        product *= calc_wins(race)
    print(product)
