from pathlib import Path

DAY = 3
INPUT_FILE = Path(f"day{DAY}/input.txt")
DEBUG = True


def load_file(fname: Path) -> list[str]:
    with open(fname) as f:
        return [x.strip() for x in f.readlines()]


def is_symbol(char: str) -> bool:
    if char.isdigit():
        return False
    if char == ".":
        return False
    return True


def check_number(
    strings: list[str],
    row: int,
    start_col: int,
    end_col: int,
) -> bool:
    """
    Checks if any of the digits surrounding the number are a 'special symbol'
    """
    input_len = len(strings)
    row_len = len(strings[row])

    # Character Before
    if is_symbol(strings[row][max(0, start_col - 1)]):
        return True

    # Character After
    if is_symbol(strings[row][min(row_len - 1, end_col + 1)]):
        return True

    # Row Above
    if row != 0:
        for x in strings[row - 1][max(0, start_col - 1) : (end_col + 2)]:
            if is_symbol(x):
                return True

    # Row Below
    if row < input_len - 1:
        for x in strings[row + 1][max(0, start_col - 1) : (end_col + 2)]:
            if is_symbol(x):
                return True

    return False


def find_digits(string: str, starting_pos: int = 0) -> tuple[int, int]:
    start: int = -1
    end: int = -1
    on_number: bool = False
    while True:
        if on_number and starting_pos >= len(string):
            end = starting_pos
            break
        if starting_pos >= len(string):
            break
        if not on_number and string[starting_pos].isdigit() and start < 0:
            start = starting_pos
            on_number = True
        if on_number and starting_pos > len(string):  # last digit is at EOL
            end = starting_pos
            break
        if on_number and not string[starting_pos].isdigit():
            end = starting_pos
            break

        starting_pos += 1

    return start, end


def process_rows(strings: list[str]):
    total = 0
    for i, line in enumerate(strings):
        last = 0
        DEBUG and print(f"{i+1}: ", end="")
        while last != -1:
            start, last = find_digits(line, last)
            # DEBUG and print(f"({start}, {last})", end=" ")
            if start > -1 and last > -1:
                DEBUG and print(line[start:last], end="")
                check = check_number(strings, i, start, last - 1)
                if check:
                    total += int(line[start:last])
                DEBUG and print("t" if check else "f", end=" ")
            else:
                DEBUG and print(f"\\ {total}")
            if last + 1 >= len(line):
                DEBUG and print(f"\\ {total}")
                break

    return total


if __name__ == "__main__":
    lines = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".split("\n")[1:]
    lines = load_file(INPUT_FILE)
    out = process_rows(lines)

    print(out)
