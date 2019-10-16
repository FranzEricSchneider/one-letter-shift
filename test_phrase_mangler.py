#!/usr/bin/python3

import pytest

from phrase_mangler import is_word, one_off_phrases, one_off_words

def test_is_word():
    for word in ["should", "halibut", "aegis", "Columns", "waTCHERS", "Ray",
                 "relevant", "REVELATION", "a", "FLy", "oRB", "cobalt", "taB",
                 "TuRKEY", "cauliflower", "CORONA", "brachiate", "Kick",
                 "Kermit"]:
        assert is_word(word)

    for not_word in ["Alabuster", "asdfa", "ABBBBRW", "CALAmitee", "JayZ",
                     "Girallon", "pilariZED", "Harly", "pANTom", "Dounds"]:
        assert not is_word(not_word)


@pytest.mark.parametrize("word, expected", (
    # Don't ask me what "acloud" is, but it"s in the dictionary :P
    ("cloud", ["acloud", "aloud", "claud", "clou", "clour", "clout", "clod", "clouds", "cloudy", "coud", "loud"]),
    # Same goes for starw and stary
    ("stars", ["scars", "sears", "sitars", "soars", "spars", "stabs", "stags", "stairs", "stans", "star", "stare", "stares", "stark", "starks", "starn", "starr", "start", "starts", "starw", "stary", "stats", "stays", "stirs", "tars"]),
))
def test_one_off_words(word, expected):
    results = one_off_words(word)
    assert len(results) == len(expected)
    for result in results:
        assert result in expected


def test_one_off_words_empty():
    with pytest.raises(AssertionError):
        one_off_words("")


def test_one_off_phrases():
    expected = (
        ["acloud stars", "aloud stars", "claud stars", "clou stars", "clour stars", "clout stars", "clod stars", "clouds stars", "cloudy stars", "coud stars", "loud stars"] +
        ["cloud scars", "cloud sears", "cloud sitars", "cloud soars", "cloud spars", "cloud stabs", "cloud stags", "cloud stairs", "cloud stans", "cloud star", "cloud stare", "cloud stares", "cloud stark", "cloud starks", "cloud starn", "cloud starr", "cloud start", "cloud starts", "cloud starw", "cloud stary", "cloud stats", "cloud stays", "cloud stirs", "cloud tars"]
    )
    results = one_off_phrases("cloud stars")
    print results
    assert len(results) == len(expected)
    for result in results:
        assert result in expected
