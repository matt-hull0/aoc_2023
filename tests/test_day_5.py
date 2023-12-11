from aoc_2023.day_5 import parse_range_through_map, parse_ranges_through_map


def test_parse_range_through_map():
    assert parse_range_through_map(
        (79, 92), {"source_range_start": 98, "dest_range_start": 50, "range_length": 2}
    ) == [(79, 92)]

    assert parse_range_through_map(
        (79, 92), {"source_range_start": 50, "dest_range_start": 52, "range_length": 48}
    ) == [(81, 94)]

    assert parse_range_through_map(
        (79, 92), {"source_range_start": 1, "dest_range_start": 52, "range_length": 2}
    ) == [(79, 92)]

    assert parse_range_through_map(
        (79, 92), {"source_range_start": 75, "dest_range_start": 65, "range_length": 10}
    ) == [(69, 74), (85, 92)]

    assert parse_range_through_map(
        (79, 92), {"source_range_start": 80, "dest_range_start": 0, "range_length": 5}
    ) == [(79, 79), (0, 4), (85, 92)]

    assert parse_range_through_map(
        (79, 92), {"source_range_start": 81, "dest_range_start": 0, "range_length": 1}
    ) == [(79, 80), (0, 0), (82, 92)]

    assert parse_range_through_map(
        (79, 92),
        {"source_range_start": 90, "dest_range_start": 70, "range_length": 100},
    ) == [(79, 89), (70, 72)]


def test_failing_assert():
    to_parse = (310_752_231, 369_330_440)
    map_row = {
        "dest_range_start": 110_580_631,
        "source_range_start": 329_763_915,
        "range_length": 34_129_824,
    }

    assert parse_range_through_map(
        to_parse,
        map_row,
    ) == [(310752231, 329763914), (110580631, 144710454), (363893739, 369330440)]


def test_parse_ranges_through_map():
    ranges_list = [(74, 87)]
    map = [
        {"dest_range_start": 45, "source_range_start": 77, "range_length": 23},
        {"dest_range_start": 81, "source_range_start": 45, "range_length": 19},
        {"dest_range_start": 68, "source_range_start": 64, "range_length": 13},
    ]

    assert parse_ranges_through_map(ranges_list, map) == [(45, 55), (78, 80)]


def test_debugging_differences_to_others():
    range_to_parse = (663_999_152, 690_558_737)
    map_row = {
        "dest_range_start": 500_989_478,
        "source_range_start": 564_295_961,
        "range_length": 163_009_674,
    }

    assert parse_range_through_map(
        range_to_parse,
        map_row,
    ) == [(600692669, 627252254)]


def test_parse_ranges_through_map():
    ranges_list = [(81, 94)]
    map = [
        {"dest_range_start": 88, "source_range_start": 18, "range_length": 7},
        {"dest_range_start": 18, "source_range_start": 25, "range_length": 70},
    ]

    assert parse_ranges_through_map(ranges_list, map) == [(74, 87)]
