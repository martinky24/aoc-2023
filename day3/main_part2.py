from pathlib import Path

DAY = 3
INPUT_FILE = Path(f"day{DAY}/input.txt")
DEBUG = False


def load_file(fname: Path) -> list[str]:
    with open(fname) as f:
        return [x.strip() for x in f.readlines()]


def find_all_asterisks(input_list: list[str]) -> list[tuple[int, int]]:
    out = []
    for i, row in enumerate(input_list):
        for j, char in enumerate(row):
            if char == "*":
                out.append((i, j))
    return out


def find_number(input_list: list[str], row: int, col: int) -> int:
    start = col
    end = col

    while True:
        if start == 0:
            break
        start -= 1
        if not input_list[row][start].isdigit():
            start += 1
            break

    while True:
        end += 1
        if end >= len(input_list[row]):
            break
        if not input_list[row][end].isdigit():
            break

    DEBUG and print(row, start, end, input_list[row][start:end])
    return int(input_list[row][start:end])


def check_asterisk_numbers(input_list: list[str], position: tuple[int, int]) -> tuple[int, int]:
    out = []
    x, y = position
    list_len = len(input_list)
    str_len = len(input_list[x])

    assert input_list[x][y] == "*"
    if input_list[x][y - 1].isdigit():
        DEBUG and print(f"1 FOUND NUMBER {x} {y-1}")
        out.append(find_number(input_list, x, y - 1))

    if input_list[x][y + 1].isdigit():
        DEBUG and print(f"2 FOUND NUMBER {x} {y+1}")
        out.append(find_number(input_list, x, y + 1))

    for val in [y - 1, y, min(y + 1, str_len)]:
        if x >= 0 and input_list[x - 1][val].isdigit():
            DEBUG and print(f"3 FOUND NUMBER {x-1} {val}")
            out.append(find_number(input_list, x - 1, val))
        if x < list_len and input_list[x + 1][val].isdigit():
            DEBUG and print(f"4 FOUND NUMBER {x+1} {val}")
            out.append(find_number(input_list, x + 1, val))

    out = list(set(out))  # delete duplicates (this is definitely a bug)
    # I REPEAT:
    # DEFINITELY A BUG!

    if len(out) != 2:
        return None

    return out[0], out[1]


def main(input_list: list[str]) -> int:
    total = 0
    astks = find_all_asterisks(input_list)
    DEBUG and print(astks)
    for x in astks:
        vals = check_asterisk_numbers(input_list, x)
        DEBUG and print(vals)
        if vals is not None:
            total += vals[0] * vals[1]
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
    out = main(lines)

    print(out)
