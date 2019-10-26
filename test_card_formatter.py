#!/usr/bin/python

import mock
import pytest

import card_formatter


def test_filter_values():
    """Check that characters and strings are replaced correctly."""
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
    card_formatter.filter_values(rows, bad_strings)
    assert rows[0]["aching"] == "Tifffany"
    assert rows[0]["corporal"] == "Carry"
    assert rows[0]["weatherwax"] == "Esmereldo"


@mock.patch('card_formatter.content_formatter')
@mock.patch('card_formatter.indexer')
def test_arranger(indexer_mock, content_mock):
    """Indices and content should be zipped together in a dictionary."""
    indexer_mock.return_value=iter(range(25, 35))
    content_mock.return_value=["a", "b"]
    arrangement = card_formatter.arranger(fields=None, rows=[10, 20],
                                          width=None, height=None)
    # The result should be of length len(content_mock)*len(rows), combining
    # whatever indexer returns with the content_mock return value
    assert arrangement == {
        25: "a", 26: "b", 27: "a", 28: "b",
    }

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
    for expected_index, index in zip(
            expected, card_formatter.indexer(width, height)):
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
    assert list(zip(range(2),
                    card_formatter.content_formatter(fields, row))) == \
        [(0, "Maurice\nEducated rodents"),
         (1, "Maurice\nWerewolf | Littlebottom | the Troll")]
