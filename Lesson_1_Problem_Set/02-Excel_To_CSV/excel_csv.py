# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    regions = [str(sheet.cell_value(0, col)) for col in range(1, 9)]
    sheet_data = [[sheet.cell_value(r, col) for r in range(sheet.nrows) if r > 0] for col in range(1, 9)]
    sheet_times = [sheet.cell_value(r, 0) for r in range(sheet.nrows) if r > 0]
    data_max = [max(col) for col in sheet_data]
    data = []
    for (i, region) in enumerate(regions):
        index = sheet_data[i].index(data_max[i])
        time_stamp = sheet_times[index]
        data.append([region])
        data[i].extend(list(xlrd.xldate_as_tuple(time_stamp, 0))[0:4])
        data[i].append(data_max[i])
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    return data


def save_file(data, filename):
    header = ["Station", "Year", "Month", "Day", "Hour", "Max Load"]
    csv.register_dialect('dialect', delimiter='|', quoting=csv.QUOTE_NONE)
    with open(outfile, 'wb') as f:
        writer = csv.writer(f, 'dialect')
        writer.writerow(header)
        for row in data:
            writer.writerow(row)


def test():
    # open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        print "ans", max_answer
                        print "line", max_line
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    test()
