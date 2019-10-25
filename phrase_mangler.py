#!/usr/bin/python3

import argparse
import string

with open("/home/eric/projects/english-words-master/words.txt") as word_file:
    WORDS = set(word.strip().lower() for word in word_file)


def is_word(potential_word):
    """Returns True if given word is found in our English dictionary."""
    return potential_word.strip().lower() in WORDS


def one_off_words(word):
    """Returns list of possible off-by-one words."""

    assert word, "Word {!r} was empty".format(word)
    word = word.strip().lower()
    results = []

    # Then check whether any substitutions get words
    for character in string.ascii_lowercase + "_":
        for index in range(len(word)):
            # Skip no-ops
            if word[index] == character:
                continue
            # Then replace the character at the given index
            test = list(word)
            test[index] = character
            # Use _ as an empty space so it can be iterated over, then remove
            test = "".join(test).replace("_", "")
            # Check whether we have a word
            if is_word(test):
                results.append(test)

    # Then check if any insertions create words
    for character in string.ascii_lowercase:
        for index in range(len(word) + 1):
            test = word[:index] + character + word[index:]
            if is_word(test):
                results.append(test)

    return sorted(results)


def one_off_phrases(phrase):
    """Returns list of phrases where one letter is off in the phrase."""
    words = phrase.split(" ")
    results = []
    for index, word in enumerate(words):
        for off_word in one_off_words(word):
            results.append(" ".join(words[:index] + [off_word] + words[index+1:]))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="Text file to permute phrases for")
    args = parser.parse_args()

    with open(args.file, "r") as phrase_file:
        while True:
            phrase = phrase_file.readline().strip().lower()
            if not phrase:
                break
            print(phrase)
            for off_phrase in one_off_phrases(phrase):
                print("\t{}".format(off_phrase))


if __name__ == "__main__":
    main()
