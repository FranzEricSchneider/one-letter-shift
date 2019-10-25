#!/usr/bin/python3

import argparse
import csv


# Problematic strings to find and replace 
BAD_STRINGS = {}


def filter_values(rows):
    for row in rows:
        for key in row:
            for bad_string in BAD_STRINGS:
                if bad_string in row[key]:
                    print("{!r} found in {}, replaced with {!r}".format(
                        bad_string, row[key], BAD_STRINGS[bad_string]
                    ))
                    row[key] = row[key].replace(bad_string,
                                                BAD_STRINGS[bad_string])


def arranger(fields, rows):
    arrangement = {
        index: content in zip(indexer(), formatter(fields, row))
        for row in rows
    }


def indexer():
    # The page is 3 cards wide and 6 cards tall
    width = 3
    height = 6

    pass


def formatter(fields, row):
    name = "Name"
    description = "Description"

    yield "{}\n{}".format(row[name], row[description])
    yield "{}\n".format(row[name]) + " | ".join(
        row[field] for field in fields if field not in [name, description]
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", help="CSV to draw card data from")
    args = parser.parse_args()

    # First get the fields
    with open(args.csv, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        fields = next(csv_reader)

    # Store all the data as a list of dicts, all with the same fields
    with open(args.csv, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        rows = [row for row in csv_reader]

    print(fields)
    print('')
    print(rows)


if __name__ == "__main__":
    main()
