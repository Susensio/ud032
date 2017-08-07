#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the
"areaLand" field, you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it
has to return a float representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you
like, but changes to process_file will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'


def fix_area(area):
    if parse_type(area) == type(list()):
        return fix_area(parse_list(area))
    else:
        try:
            area = float(area)
        except ValueError:
            area = None
        return area


def parse_list(values):
    values_list = values.strip("{}").split("|")
    values_list.sort(key=lambda x: -len(x))
    return values_list[0]


def parse_type(value):
    if value == "NULL" or value == "":
        return type(None)
    elif value[0] is "{":
        return type(list())
    else:
        try:
            int(value)
            return type(int())
        except ValueError:
            pass
        try:
            float(value)
            return type(float())
        except ValueError:
            pass
    return type(str())


def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        # skipping the extra metadata
        for _ in range(3):
            _ = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])

            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5, 8):
        pprint.pprint(data[n]["areaLand"])

    assert data[3]["areaLand"] == None
    assert data[8]["areaLand"] == 55166700.0
    assert data[20]["areaLand"] == 14581600.0
    assert data[33]["areaLand"] == 20564500.0


if __name__ == "__main__":
    test()
