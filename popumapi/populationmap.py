""" Defines PopulationMap and GeoTiffMap. """

import abc
import math
from typing import Tuple
import rasterio
from rasterio.coords import BoundingBox
from popumapi.coords import Coords


class PopulationMap(abc.ABC):
    """ Contract for a population map. """
    @abc.abstractmethod
    def coords_in_bounds(self, coords: Coords) -> bool:
        """ Returns True if the coordinates lie inside the map.

        Parameters
        ----------
            coords : longitude,latitude in decimal degrees.
        """
        pass

    @abc.abstractmethod
    def compute_population(self, coords: Coords, radius: int) -> int:
        """ Compute the population within a radius on the map.

        Parameters
        ----------
            coords : longitude,latitude in decimal degrees.
            radius : The radius rounded to the nearest km.

        Returns
        -------
            A `float`; the estimated population in the area, rounded up.

        Raises
        ------
            `ValueError`: If the coordinates do not lie in the map
        """
        pass


class GeoTiffMap(PopulationMap):
    """ Implements PopulationMap using a WorldPop GeoTiff file.

    Dataset files that can be used with this class can be found online:
    https://www.worldpop.org/

    This class assumes the GeoTiff file has the following properties:
        * Single band holding the population data.
        * Coordinate Reference System: "EPSG 4326"
        * The raster is in the "North-Up" position
        * Specific transform: a, d = +-0.0008333333300826796
            which, together with the coordinate reference system gives
            a resolution of around 100m per cell
    """

    _file_name: str
    _bounds: BoundingBox
    _width: int
    _height: int

    def __init__(self, file_name):
        """ Initializes a geotiffMap.

        Parameters
        ----------
            file_name: The path to the geotiff file.
        """
        self._file_name = file_name
        with rasterio.open(file_name) as context:
            self._ctx = context
            self._bounds = context.bounds
            self._width = context.width
            self._height = context.height

    def coords_in_bounds(self, coords: Coords):
        """ See base class. """
        x, y = coords
        return (self._bounds.left < x < self._bounds.right
                and self._bounds.bottom < y < self._bounds.top)

    def compute_population(self, coords: Coords, radius: int):
        """ See base class. """

        if not self.coords_in_bounds(coords):
            raise ValueError("Coordinates not in map")

        with rasterio.open(self._file_name) as context:
            x, y = coords
            # Transform coordinates to grid location
            origin = context.index(x, y)

            # With a resolution of 100m, 1 km covers around 10 grid cells
            r_in_units = 10 * radius

            arr = context.read(1)

            s = sum(arr[v] for v in self._indices_in_r(origin, r_in_units)
                    if arr[v] > 0)
            return math.ceil(s)

    def _indices_in_r(self, origin, radius):
        """ Yields all indices of circle within pop map. """
        return indices_in_radius(origin, radius, self._width, self._height)


def indices_in_radius(origin: Tuple[int, int], radius: int, width: int,
                      height: int):
    """ Yields a row,col Tuple within radius, width and height.

    The row index will always be between 0 and width.
    The col index will always be between 0 and height.
    """
    x, y = origin

    left_bound = max(x - radius, 0)
    right_bound = min(x + radius, width)
    lower_bound = max(y - radius, 0)
    upper_bound = min(y + radius, height)

    for i in range(left_bound, right_bound):
        for j in range(lower_bound, upper_bound):
            if (i - x)**2 + (j - y)**2 < radius**2:
                yield i, j
