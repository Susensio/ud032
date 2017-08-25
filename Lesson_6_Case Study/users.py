#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

OSMFILE = "example.osm"
ZGZFILE = "C:\data\zaragoza_xml.osm"


def get_user(element):
    return element.attrib['uid']


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == "node":
            users.add(get_user(element))

    return users


def test():

    users = process_map(ZGZFILE)
    pprint.pprint(len(users))
    # assert len(users) == 4


if __name__ == "__main__":
    test()
