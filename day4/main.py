from pathlib import Path

DAY = 4
INPUT_FILE = Path(f"day{DAY}/input.txt")
DEBUG = True


def load_file(fname: Path) -> list[str]:
    with open(fname) as f:
        return [x.strip() for x in f.readlines()]


def load_cards(lines: list[str]) -> list[list[set[str]]]:
    cards = [line.split(":")[1] for line in lines]
    cards = [line.split("|") for line in cards]
    for card in cards:
        card[0] = set(card[0].strip().split(" "))
        if "" in card[0]:
            card[0].remove("")
        card[1] = set(card[1].strip().split(" "))
        if "" in card[1]:
            card[1].remove("")
    return cards


def process_cards(cards: list[list[set[str]]]) -> int:
    total = 0
    for card in cards:
        print(card)
        results = card[0].intersection(card[1])
        print(results)
        count = 2 ** (len(results) - 1) if 2 ** (len(results) - 1) >= 1 else 0
        print(count)
        total += count
    return total


if __name__ == "__main__":
    lines = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".split("\n")[1:]
    lines = load_file(INPUT_FILE)
    out = load_cards(lines)
    out = process_cards(out)
    print(out)
