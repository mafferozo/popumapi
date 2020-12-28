# Popumapi: Population density api.

Compute population density based on place name and radius.

## API Description

GET /population?location={}&radius={}

The general idea:

- Compute Population Density rasters for parts of the earth (worldpop.org)
- Compute a hashmap to find geocoordinates of locations based on keywords (geonames)

- Given a geocoordinate, radius and a set of Population maps:
  - Choose the map that yields the best approximation based on the geocoordinate and radius
  - Transform the geocoordinate to an index in the map; x0, y0
  - Sum the cells of the map that lie inside the circle with origin x0,y0 and the given radius.

## Problem area's:

- Computing a rasterized density map of an area
- Summing all cells inside a circle of the raster
- Geocoding the input city or address

Extract points from raster given a base point and radius

```Python
from numpy import *

def points_in_circle(circle, arr):
    "A generator to return all points whose indices are within given circle."
    i0,j0,r = circle
    def intceil(x):
        return int(ceil(x))
    for i in xrange(intceil(i0-r),intceil(i0+r)):
        ri = sqrt(r**2-(i-i0)**2)
        for j in xrange(intceil(j0-ri),intceil(j0+ri)):
            yield arr[i][j]
```

## Affine Coordinate transform:

From georeferenced coordinate to raster position:

```
Xgeo = GT(0) + Xpixel*GT(1) + Yline*GT(2)
Ygeo = GT(3) + Xpixel*GT(4) + Yline*GT(5)
```

In the simple case of North-Up rasters, GT(2) = 0 and GT(4) = 0
Locating a geocoordinate in terms of Xpixel and Yline in the simple case:

```
Xpixel = (Xgeo - GT(0)) / GT(1)
Yline = (Ygeo - GT(3)) / GT(5)
```

### WorldPop project:

- [General info](https://www.worldpop.org/methods/populations)
- [Top down versus bottom-up approach](https://www.worldpop.org/methods/populations)

### Research links:

- [Global spatio-temporally harmonised datasets for producing high-resolution gridded population distribution datasets](https://www.tandfonline.com/doi/full/10.1080/20964471.2019.1625151) - The method used for computing the grid.
- [Classical models of urban population density, applied to Barcelona Metropolitan Area](https://www.researchgate.net/publication/23730354_Classical_models_of_urban_population_density_The_case_of_Barcelona_Metropolitan_Area)
- [Population index from multi-sensor image data](https://www.tandfonline.com/doi/abs/10.1080/09595237500185051)
