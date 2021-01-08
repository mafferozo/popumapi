""" Defines Population """

from typing import List
from popumapi import coords, populationmap


class Population:
    """ Population class """
    loc_map: dict
    pop_maps: List[populationmap.PopulationMap]

    def __init__(self, loc_map, pop_maps):
        """ Initalizes the population mapping object.

        Parameters
        ----------
            loc_map: `dict` object that maps strings to coords.
            pop_maps: `list` object with maps to compute population
        """
        self.loc_map = loc_map
        self.pop_maps = pop_maps

    def compute_population(self, loc: str, radius: int):
        """ Computes the population in a radius around location.

        Parameters
        ----------
            loc: location string.
            radius: `int` in km.

        Returns
        -------
            A `dictionary` with coords, population_count or error message
        """
        co = self.get_coords(loc)
        if co is not None:
            print("Found coordinates: ", co)
            pop_map = self.choose_population_map(co)
            if pop_map is not None:
                return {
                    "coords": co,
                    "population_count": pop_map.compute_population(co, radius),
                }
        return {"error_message": "Couldn't find coordinate for given location"}

    def choose_population_map(self, c: coords.Coords):
        """ Choose a population map that yields the best approximation.

        For now, just return the first map that has the point inside
        its boundary.
        """
        return next(map for map in self.pop_maps if map.coords_in_bounds(c))

    def get_coords(self, loc: str):
        """ Get the coordinates from the location map.

        For now, a simple hashmap lookup.
        """
        return self.loc_map.get(loc.lower())
