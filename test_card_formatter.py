#!/usr/bin/python3

import pytest

from card_formatter import arranger, filter_values, content_formatter, indexer


def test_filter_values():
    rows = [{
        "aching": "TifFany",
        "corporal": "Carrot",
        "weatherwax": "EsmereldA",
    }]
    bad_strings = {
        "rot": "ry",
        "A": "o",
        "F": "ff",
    }
    filter_values(rows, bad_strings)
    assert rows[0]["aching"] == "Tifffany"
    assert rows[0]["corporal"] == "Carry"
    assert rows[0]["weatherwax"] == "Esmereldo"


def test_arranger():
    pass


@pytest.mark.parametrize("expected, width, height", (
    ([0,  20, 1,  19, 2,  18,
      3,  23, 4,  22, 5,  21,
      6,  26, 7,  25, 8,  24,
      9,  29, 10, 28, 11, 27,
      12, 32, 13, 31, 14, 30,
      15, 35, 16, 34, 17, 33,
      36, 56, 37, 55, 38, 54], 3, 6),
    ([0, 14, 1, 13, 2, 12, 3, 11, 4, 10,
      5, 19, 6, 18, 7, 17, 8, 16, 9, 15,
      20, 34, 21, 33, 22, 32, 23, 31, 24, 30], 5, 2),
))
def test_indexer(expected, width, height):
    """Check double-sided indices with several page sizes, wrapping pages."""
    for expected_index, index in zip(expected, indexer(width, height)):
        assert expected_index == index


def test_content_formatter():
    """Test that name/description are right, then everything is appended."""
    fields = ["Name", "Description", "Angua", "Cheery", "Detritus"]
    row = {
        "Name": "Maurice",
        "Description": "Educated rodents",
        "Angua": "Werewolf",
        "Cheery": "Littlebottom",
        "Detritus": "the Troll",
    }
    assert list(zip(range(2), content_formatter(fields, row))) == \
        [(0, "Maurice\nEducated rodents"),
         (1, "Maurice\nWerewolf | Littlebottom | the Troll")]
