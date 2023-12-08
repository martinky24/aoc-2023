from pathlib import Path

DAY = 2
INPUT_FILE = Path(f"day{DAY}/input.txt")


def load_file(fname: Path) -> list[str]:
    with open(fname) as f:
        return [x.strip() for x in f.readlines()]


def main():
    lines = load_file(INPUT_FILE)
    del lines


if __name__ == "__main__":
    main()
