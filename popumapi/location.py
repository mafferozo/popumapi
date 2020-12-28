""" Defines a TSV parser"""
from popumapi import coords


def add_file_to_map(map_obj, file):
    """ Parses TSV text file with location, latitude and longitude information.

    TSV is specified in: http://download.geonames.org/export/dump/readme.txt

    Returns
    -------
        A `dict` object with string keys as location and `Coords` as value
    """
    with open(file) as f:
        lines = [line.split("\t") for line in f.readlines()]
        for line in lines:
            key = line[1].lower()
            point = coords.Coords(float(line[5]), float(line[4]))
            map_obj[key] = point
    return map_obj
