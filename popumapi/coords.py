""" Defines Coords class, a NamedTuple. """

from typing import NamedTuple

_Coords = NamedTuple("Coords", [("x", float), ("y", float)])


class Coords(_Coords):
    """ A Tuple (x,y) that defines a place on the earth. """
    @property
    def longitude(self):
        """
        Latitude in decimal degrees
        """
        return self.x

    @property
    def latitude(self):
        """
        Longitude in decimal degrees
        """
        return self.y
