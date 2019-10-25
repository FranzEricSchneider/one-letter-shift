#!/usr/bin/python3

from card_formatter import arranger, filter_values, formatter, indexer


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


def test_indexer():
    expected = ([0,  20], [1,  19], [2,  18],
                [3,  23], [4,  22], [5,  21],
                [6,  26], [7,  25], [8,  24],
                [9,  29], [10, 28], [11, 27],
                [12, 32], [13, 31], [14, 30],
                [15, 35], [16, 34], [17, 33],
                [36, 56], [37, 55], [38, 54])

    for expected_indices, indices in zip(expected, indexer()):
        assert len(indices) == 2
        assert expected_indices[0] == indices[0]
        assert expected_indices[1] == indices[1]


def test_formatter():
    fields = ["Name", "Description", "Angua", "Cheery", "Detritus"]
    row = {
        "Name": "Maurice",
        "Description": "Educated rodents",
        "Angua": "Werewolf",
        "Cheery": "Littlebottom",
        "Detritus": "the Troll",
    }
    assert list(zip(range(2), formatter(fields, row))) == \
        [(0, 'Maurice\nEducated rodents'),
         (1, 'Maurice\nWerewolf | Littlebottom | the Troll')]
