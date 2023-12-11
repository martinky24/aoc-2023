import multiprocessing as mp
import time
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from queue import Empty

DAY = 5
INPUT_FILE = Path(f"day{DAY}/input.txt")


def load_file(fname: Path) -> list[str]:
    with open(fname) as f:
        return [x.strip() for x in f.readlines()]


@dataclass
class SeedRange:
    seed_start: int
    seed_range: int


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


def get_seeds(lines: list[str]) -> tuple[list[SeedRange], list[str]]:
    seeds = lines[0].split(":")[1].strip().split(" ")
    remaining_lines = lines[2:]
    seeds = [int(x) for x in seeds]
    seed_ranges = []
    for ct in range(0, len(seeds), 2):
        seed_ranges.append(SeedRange(seed_start=seeds[ct], seed_range=seeds[ct + 1]))
    return seed_ranges, remaining_lines


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


class LocationSolver(mp.Process):
    def __init__(
        self,
        seed_range: SeedRange,
        seeds_to_soil: list[Mapping],
        soil_to_fertilizer: list[Mapping],
        fertilizer_to_water: list[Mapping],
        water_to_light: list[Mapping],
        light_to_temperature: list[Mapping],
        temperature_to_humidity: list[Mapping],
        humidity_to_location: list[Mapping],
        result_queue: mp.Queue,
    ) -> None:
        super().__init__()
        self.seed_range = seed_range
        self.seeds_to_soil = seeds_to_soil
        self.soil_to_fertilizer = soil_to_fertilizer
        self.fertilizer_to_water = fertilizer_to_water
        self.water_to_light = water_to_light
        self.light_to_temperature = light_to_temperature
        self.temperature_to_humidity = temperature_to_humidity
        self.humidity_to_location = humidity_to_location
        self.result_queue = result_queue

    def run(self) -> None:
        self.result_queue.put(self.get_lowest())

    def get_lowest(
        self,
    ) -> tuple[int, int]:
        min_val = 10**20  # arbitrary high number
        start = self.seed_range.seed_start
        for x in range(start, start + self.seed_range.seed_range):
            mapping = get_seed_mapping(
                x,
                self.seeds_to_soil,
                self.soil_to_fertilizer,
                self.fertilizer_to_water,
                self.water_to_light,
                self.light_to_temperature,
                self.temperature_to_humidity,
                self.humidity_to_location,
            )
            if mapping.location < min_val:
                min_val = mapping.location
        return self.seed_range.seed_start, min_val


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
    # print("SEEDS: ", seeds)
    total = sum(x.seed_range for x in seeds)

    seeds_to_soil, lines = get_entries(lines, "seed-to-soil")
    soil_to_fertilizer, lines = get_entries(lines, "soil-to-fertilizer")
    fertilizer_to_water, lines = get_entries(lines, "fertilizer-to-water")
    water_to_light, lines = get_entries(lines, "water-to-light")
    light_to_temperature, lines = get_entries(lines, "light-to-temperature")
    temperature_to_humidity, lines = get_entries(lines, "temperature-to-humidity")
    humidity_to_location, lines = get_entries(lines, "humidity-to-location")

    min_vals = []

    start = time.perf_counter()
    result_queue = mp.Queue()
    processes: list[mp.Process] = []
    for seed_range in seeds:
        solver_process = LocationSolver(
            seed_range,
            seeds_to_soil,
            soil_to_fertilizer,
            fertilizer_to_water,
            water_to_light,
            light_to_temperature,
            temperature_to_humidity,
            humidity_to_location,
            result_queue,
        )
        solver_process.start()
        processes.append(solver_process)

    while True:
        try:
            returned = result_queue.get(False)
            print(time.perf_counter() - start, "\t", returned[0], returned[1])
            min_vals.append(returned[1])
        except Empty:
            pass
        alive = [(not process.is_alive()) for process in processes]
        if all(alive):
            break
        time.sleep(len(processes) / 10)

    for process in processes:
        assert not process.is_alive()

    while not result_queue.empty():
        try:
            returned = result_queue.get(False)
            print(time.perf_counter() - start, "\t", returned[0], returned[1])
            min_vals.append(returned[1])
        except Empty:
            pass

    pprint(time.perf_counter() - start)

    print("MIN_VAL: ", min(min_vals))

# Brute Force Baby 8-)

# $ caffeinate -i python day5/main_part2.py
# 53.229852250020485 	 1116624626 2324727144
# 461.80535462498665 	 221434439 811357076
# 852.1766852919827 	 1263068588 2369814041
# 1133.2649859999656 	 1368516778 1153910022
# 1650.6263577499776 	 3326254382 1410417517
# 1799.5826147500193 	 2946842531 199602917
# 2162.0494907500106 	 2098781025 427916782
# 2185.28141520801 	 3713929839 369762033
# 3003.4036244999734 	 2361566863 2254686
# 4516.481088041968 	 1576631370 95285571
# 4516.481377332995
# MIN_VAL:  2254686
