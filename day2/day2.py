from pathlib import Path
from pprint import pprint

DAY = 2
INPUT_FILE = Path(f"day{DAY}/input.txt")

MAXES = {"red": 12, "green": 13, "blue": 14}
COLORS = list(MAXES.keys())


def load_file(fname: Path) -> list[str]:
    with open(fname) as f:
        return [x.strip() for x in f.readlines()]


def parse_colors(colors: str):
    color_dict = {x.split(" ")[1]: int(x.split(" ")[0]) for x in colors}
    return color_dict


def parse_draw(draw: str):
    colors = draw.split(", ")
    # colors = [ for x in d]
    return parse_colors(colors)


def parse_game(game: str):
    games = game.split("; ")
    draws = [parse_draw(x) for x in games]
    return draws


def parse_lines(lines: list[str]):
    lines = [x.split(": ") for x in lines]
    lines_dict = {int(x[0][5:]): parse_game(x[1]) for x in lines}
    return lines_dict


def get_maxes(lines: list[str]):
    max_dict = {}
    parsed_lines = parse_lines(lines)
    for k, v in parsed_lines.items():
        max_dict[k] = {x: 0 for x in COLORS}
        for draw in v:
            for color in COLORS:
                if (max_val := draw.get(color, 0)) >= max_dict[k][color]:
                    # print(color, ":", max_val)
                    max_dict[k][color] = max_val
    return max_dict


def check_maxes(lines: list[str]):
    out = []
    maxes = get_maxes(lines)
    for g_number, game_maxes in maxes.items():
        # print("maxes: ", game_maxes)
        if all(game_maxes[color] <= MAXES[color] for color in COLORS):
            out.append(g_number)
    return out


if __name__ == "__main__":
    lines = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]
    lines = load_file(INPUT_FILE)
    # lines = [
    #     "Game 85: 15 green, 2 blue, 11 red; 4 red, 7 blue, 6 green; 3 blue, 14 green; 10 green, 10 blue, 7 red; 17 red, 3 green, 15 blue"
    # ]
    print(lines)
    pprint(get_maxes(lines))
    total = check_maxes(lines)
    print(total)
    print(sum(total))
