from dataclasses import dataclass
from pathlib import Path
from pprint import pprint


DAY = 5
INPUT_FILE = Path(f"day{DAY}/input.txt")


def load_file(fname: Path) -> list[str]:
    with open(fname) as f:
        return [x.strip() for x in f.readlines()]


@dataclass
class Mapping:
    name: str
    destination_start: int
    destination_stop: int
    source_start: int
    source_stop: int
    range_length: int


@dataclass
class SeedMapping:
    seed: int = -1  # -1 means unset, not a valid number
    soil: int = -1  # -1 means unset, not a valid number
    fertilizer: int = -1  # -1 means unset, not a valid number
    water: int = -1  # -1 means unset, not a valid number
    light: int = -1  # -1 means unset, not a valid number
    temperature: int = -1  # -1 means unset, not a valid number
    humidity: int = -1  # -1 means unset, not a valid number
    location: int = -1  # -1 means unset, not a valid number


def get_seeds(lines: list[str]):
    seeds = lines[0].split(":")[1].strip().split(" ")
    remaining_lines = lines[2:]
    seeds = [int(x) for x in seeds]
    return seeds, remaining_lines


def get_entries(lines: list[str], name: str) -> tuple[list[Mapping], list[str]]:
    lines = list(reversed(lines))
    assert (line_name := lines.pop())[: len(name)] == name, line_name
    out = []
    while lines and (line := lines.pop()) != "":
        dest, source, range_len = line.split(" ")
        range_len = int(range_len)
        seed_to_soil = Mapping(
            name=line_name,
            destination_start=int(dest),
            destination_stop=int(dest) + range_len - 1,
            source_start=int(source),
            source_stop=int(source) + range_len - 1,
            range_length=range_len,
        )
        out.append(seed_to_soil)
    return out, list(reversed(lines))


def get_mapping(value: int, mappings: list[Mapping]) -> int:
    for map in mappings:
        if map.source_start <= value <= map.source_stop:
            diff = value - map.source_start
            return map.destination_start + diff
    return value


def get_seed_mapping(
    seed_number: int,
    seeds_to_soil: list[Mapping],
    soil_to_fertilizer: list[Mapping],
    fertilizer_to_water: list[Mapping],
    water_to_light: list[Mapping],
    light_to_temperature: list[Mapping],
    temperature_to_humidity: list[Mapping],
    humidity_to_location: list[Mapping],
) -> SeedMapping:
    seed_mapping = SeedMapping()

    seed_mapping.seed = seed_number
    seed_mapping.soil = get_mapping(seed_mapping.seed, seeds_to_soil)
    seed_mapping.fertilizer = get_mapping(seed_mapping.soil, soil_to_fertilizer)
    seed_mapping.water = get_mapping(seed_mapping.fertilizer, fertilizer_to_water)
    seed_mapping.light = get_mapping(seed_mapping.water, water_to_light)
    seed_mapping.temperature = get_mapping(seed_mapping.light, light_to_temperature)
    seed_mapping.humidity = get_mapping(seed_mapping.temperature, temperature_to_humidity)
    seed_mapping.location = get_mapping(seed_mapping.humidity, humidity_to_location)
    return seed_mapping


if __name__ == "__main__":
    lines = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".split("\n")[1:]
    lines = load_file(INPUT_FILE)
    seeds, lines = get_seeds(lines)
    print("SEEDS: ", seeds)

    seeds_to_soil, lines = get_entries(lines, "seed-to-soil")
    soil_to_fertilizer, lines = get_entries(lines, "soil-to-fertilizer")
    fertilizer_to_water, lines = get_entries(lines, "fertilizer-to-water")
    water_to_light, lines = get_entries(lines, "water-to-light")
    light_to_temperature, lines = get_entries(lines, "light-to-temperature")
    temperature_to_humidity, lines = get_entries(lines, "temperature-to-humidity")
    humidity_to_location, lines = get_entries(lines, "humidity-to-location")

    # pprint(seeds_to_soil)
    # pprint(soil_to_fertilizer)
    # pprint(fertilizer_to_water)
    # pprint(water_to_light)
    # pprint(light_to_temperature)
    # pprint(temperature_to_humidity)
    # pprint(humidity_to_location)

    seed_mappings = [
        get_seed_mapping(
            seed_num,
            seeds_to_soil,
            soil_to_fertilizer,
            fertilizer_to_water,
            water_to_light,
            light_to_temperature,
            temperature_to_humidity,
            humidity_to_location,
        )
        for seed_num in seeds
    ]
    # pprint(seed_mappings)

    lowest = min(x.location for x in seed_mappings)
    pprint(lowest)
