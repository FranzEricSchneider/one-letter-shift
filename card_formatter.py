#!/usr/bin/python3

import argparse
import csv



# Problematic strings to find and replace 
BAD_STRINGS = {}


def filter_values(rows, bad_strings):
    for row in rows:
        print("row", row)
        for key in row:
            print("key", key)
            for bad in bad_strings:
                print("bad", bad)
                print("row[key]", row[key])
                if bad in row[key]:
                    print("{!r} found in {}, replaced with {!r}".format(
                        bad, row[key], bad_strings[bad]
                    ))
                    row[key] = row[key].replace(bad, bad_strings[bad])


# This doesn't quite work
def arranger(fields, rows):
    arrangement = {}

    for row in rows:
        indices = indexer()
        for index in indices:
            arrangement[index] = formatter(fields, row)

    return arrangement


def indexer():
    # The page is 3 cards wide and 6 cards tall
    width = 3
    height = 6
    page = width * height

    counter = 0

    while True:
        width_offset = int(((counter % width) - (width - 1) /  2.0) * -2)

        yield (counter,
               counter + page + width_offset)
        counter += 1

        # When we've filled the front and backside of a page, skip two pages
        if counter % page == 0:
            counter += page


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

    print(arranger(fields, rows))


if __name__ == "__main__":
    main()
