from pathlib import Path

NUM_REPLACEMENTS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

ALL_VALS = list(NUM_REPLACEMENTS.keys()) + list(NUM_REPLACEMENTS.values())


def load_file(fname: Path) -> list[str]:
    with open(fname) as f:
        return [x.strip() for x in f.readlines()]


def find_first(line: str) -> str:
    min_val = 1e9
    for x in ALL_VALS:
        pos = line.find(x)
        if pos == -1:
            continue
        if pos < min_val:
            min_val = pos
            to_return = NUM_REPLACEMENTS.get(x, x)
    return to_return


def find_last(line: str) -> str:
    max_val = -2
    for x in ALL_VALS:
        pos = line.rfind(x)
        if pos == -1:
            continue
        if pos > max_val:
            max_val = pos
            to_return = NUM_REPLACEMENTS.get(x, x)
    return to_return


def get_calibration_value(line: str) -> int:
    print(f"{line}, {int(find_first(line) + find_last(line))}")
    return int(find_first(line) + find_last(line))


def main(fname: Path) -> int:
    lines = load_file(fname)
    cal_vals = [get_calibration_value(line) for line in lines]
    return sum(cal_vals)


if __name__ == "__main__":
    file = Path("day1/input.txt")
    assert file.exists()
    output = main(file)
    print(output)

    # vals = [
    #     "two1nine",
    #     "eightwothree",
    #     "abcone2threexyz",
    #     "xtwone3four",
    #     "4nineeightseven2",
    #     "zoneight234",
    #     "7pqrstsixteen",
    # ]
    # print(sum(get_calibration_value(line) for line in vals))
