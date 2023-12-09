from dataclasses import dataclass
from pathlib import Path


@dataclass
class hand:
    hand_number: int
    winning_numbers: set[int]
    my_numbers: set[int]
    copies: int = 1
    points: int = 0


DAY = 4
INPUT_FILE = Path(f"day{DAY}/input.txt")
DEBUG = True


def load_file(fname: Path) -> list[str]:
    with open(fname) as f:
        return [x.strip() for x in f.readlines()]


def load_cards(lines: list[str]) -> dict[int, hand]:
    out_cards = {}
    cards = [line.split(":")[1] for line in lines]
    cards = [line.split("|") for line in cards]
    for i, card in enumerate(cards):
        hand_number = i + 1

        winners = set(card[0].strip().split(" "))
        if "" in winners:
            winners.remove("")
        my_numbers = set(card[1].strip().split(" "))
        if "" in my_numbers:
            my_numbers.remove("")
        this_hand = hand(
            hand_number=hand_number,
            winning_numbers=winners,
            my_numbers=my_numbers,
        )
        out_cards[hand_number] = this_hand

    return out_cards


def process_cards(cards: dict[int, hand]) -> int:
    for this_hand in cards.values():
        results = this_hand.winning_numbers.intersection(this_hand.my_numbers)
        this_hand.points = len(results)
        for _ in range(this_hand.copies):
            for i in range(this_hand.points):
                cards[this_hand.hand_number + i + 1].copies += 1
    return sum(x.copies for x in cards.values())


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
