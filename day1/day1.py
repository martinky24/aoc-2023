from pathlib import Path


def load_file(fname: Path) -> list[str]:
    with open(fname) as f:
        return f.readlines()


def get_calibration_value(line: str) -> int:
    first = None
    last = None
    for x in line:
        if x.isdigit():
            if first is None:
                first = x
            last = x
    return int(first + last)


def main(fname: Path) -> int:
    lines = load_file(fname)
    cal_vals = [get_calibration_value(line) for line in lines]
    return sum(cal_vals)


if __name__ == "__main__":
    file = Path("day1/input.txt")
    assert file.exists()
    output = main(file)
    print(output)
