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
    for row in rows:
        for key in row:
            for bad in bad_strings:
                if bad in row[key]:
                    print("{!r} found in {}, replaced with {!r}".format(
                        bad, row[key], bad_strings[bad]
                    ))
                    row[key] = row[key].replace(bad, bad_strings[bad])


def arranger(fields, rows, width, height):
    """TODO"""

    arrangement = {}

    index_generator = indexer(width, height)
    for row in rows:
        for content in content_formatter(fields, row):
            arrangement[next(index_generator)] = content

    return arrangement


def indexer(width, height):
    """TODO"""

    page = width * height
    counter = 0

    while True:
        yield counter

        width_offset = int(((counter % width) - (width - 1) /  2.0) * -2)
        yield counter + page + width_offset

        counter += 1

        # When we've filled the front and backside of a page, skip two pages
        if counter % page == 0:
            counter += page


def content_formatter(fields, row):
    """TODO"""

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
    parser.add_argument("csv", help="CSV to draw card data from")
    parser.add_argument("-f", "--to-file",
                        help="Writes tex code to text.tex instead of printing",
                        action="store_true")
    args = parser.parse_args()

    # First get the fields
    with open(args.csv, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        fields = next(csv_reader)

    # Store all the data as a list of dicts, all with the same fields
    with open(args.csv, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        rows = [row for row in csv_reader]

    card_formatter(arranger(fields, rows, width=3, height=6),
                   width=3,
                   to_file=args.to_file)


if __name__ == "__main__":
    main()
