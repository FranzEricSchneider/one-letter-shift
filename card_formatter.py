#!/usr/bin/python3

"""
TODO:
    Polish the tests and docstrings

    Sort things appropriately by level and interest
    Color code the boxes
    Make a mechanism for bolding things
    Get the color highlighting right for the right fields (LaTeX first)
    Format school and labels differently
"""

import argparse
import csv

# Problematic strings to find and replace
BAD_STRINGS = {}


def filter_values(rows, bad_strings):
    """Search through rows and remove bad string snippets.

    Useful when taking something automatically exported from the spreadsheet
    that you don't want to clean by hand.

    Arguments:
        rows: list of dictionaries, form {"field name": "content string"}.
            The content strings are what are searched
        bad_strings: dictionary of {"search string": "replace string"}

    Returns:
        Nothing. Modifies rows in place
    """
    for row in rows:
        for key in row:
            for bad in bad_strings:
                if bad in row[key]:
                    print("{!r} found in {}, replaced with {!r}".format(
                        bad, row[key], bad_strings[bad]
                    ))
                    row[key] = row[key].replace(bad, bad_strings[bad])


def arranger(fields, rows, width, height):
    """Returns dictionary of final card page index to content.

    Arguments:
        fields: list of strings, length n, where the fields and the keys of
            the row dictionary are 1:1. The order of fields determines how
            things will be displayed
        rows: list of dictionaries, form {"field name": "content string"}
        width: integer, number of cards wide on a page
        height: integer, number of cards high on a page

    Returns:
        Dictionary of {index (int): "formatted content"}, where the index
            refers to the final page index
    """
    arrangement = {}
    # Dynamically assign indices to the front and back sides of card content
    index_generator = indexer(width, height)
    for row in rows:
        for content in content_formatter(fields, row):
            arrangement[next(index_generator)] = content
    return arrangement


def indexer(width, height):
    """Generator, yields indices in order to allow double-sided printing

    The reference frame has index 0 in the upper left, then counts up to the
    right, wraps, and counts up as you go down the page. As if you were
    reading. If the pages were 3x2, the order would be
        0   8    1   7    2   6
        3   11   4   10   5   9
    This would place the first and second indices on top of each other when
    they are printed double-sided, since the indices 5->6 switches to the next
    page.

    Arguments:
        width: integer, number of cards wide on a page
        height: integer, number of cards high on a page

    Yields:
        Integer index of the card on double-sided printed paper
    """
    page = width * height
    counter = 0
    while True:
        # The index for the front page (simple)
        yield counter
        # The index for the back page needs to be flipped across the vertical
        # axis, takes a more complicated calculation
        width_offset = int(((counter % width) - (width - 1) /  2.0) * -2)
        yield counter + page + width_offset
        # Bookkeep
        counter += 1
        # When we've filled the front and backside of a page, skip a page
        if counter % page == 0:
            counter += page


def content_formatter(fields, row):
    """Generator, yields content for front and back sides of a card

    Arguments:
        fields: list of strings, length n, where the fields and the keys of
            the row dictionary are 1:1. The order of fields determines how
            things will be displayed
        row: dictionary of {"field name": "content"}, where "Name" and
            "Description" must be populated

    Yields:
        Two strings, first the front side of the card, then the back
    """

    name = "Name"
    description = "Description"

    yield "{}\n{}".format(row[name], row[description])
    yield "{}\n".format(row[name]) + " | ".join(
        row[field] for field in fields if field not in [name, description]
    )


def card_formatter(arrangement, width, to_file=False):
    """TODO"""

    # Get the max index that we have to fill up to
    max_index = max(arrangement.keys())

    formatted = ""
    for index in range(max_index + 1):
        if index > 0 and index % width == 0:
            formatted += "\par\n"

        if index in arrangement:
            formatted += "\mybox{" + arrangement[index].replace("\n", "\par{}") + "}\n"
        else:
            formatted += "\mybox{}\n"

    if to_file:
        with open("text.tex", "w") as out_file:
            out_file.write(formatted)
        print("Wrote to text.tex")
    else:
        print(formatted)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv",
                        help="CSV to draw card data from")
    parser.add_argument("-f", "--to-file",
                        help="Writes tex code to text.tex instead of printing",
                        action="store_true")
    args = parser.parse_args()

    # First get the fields
    with open(args.csv, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        fields = next(csv_reader)

    # Store all the data as a list of dicts, all with the same field keys
    with open(args.csv, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        rows = [row for row in csv_reader]

    # If we have something to look for, filter
    if BAD_STRINGS:
        filter_values(rows, BAD_STRINGS)

    # Print or write the content out, depending on args
    card_formatter(arranger(fields, rows, width=3, height=6),
                   width=3,
                   to_file=args.to_file)


if __name__ == "__main__":
    main()
