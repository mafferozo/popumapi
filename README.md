# Popumapi: Population density api.

Determine population based on a place name and radius.

## The general idea:

- Generate Population Density rasters for parts of the earth (worldpop.org)
- Create a hashmap to find geocoordinates of locations based on keywords (geonames)
- Given a geocoordinate, radius and a set of Population maps:
  - Choose the map that yields the best approximation based on the geocoordinate and radius
    Smaller maps with higher resolution could give more accurate results for small radius, but is infeasible for large radius.
  - Transform the geocoordinate to an index in the map; x0, y0
  - Sum the cells of the map that lie inside the circle with origin x0,y0 and the given radius.

## Problem area's:

- Computing a rasterized density map of an area
- Summing all cells inside a circle of the raster
- Geocoding the input city or address

# API Description

The api is just a single GET request with 2 query parameters:

`GET /population?location={}&radius={}`

example response:

```json
{
  "location": "Utrecht",
  "radius": "10 km",
  "response": { "coords": [5.12222, 52.09083], "population_count": 432599 }
}
```

# Usage and Installation

This project makes use of rasterio. The easiest way to get it running is by creating a conda virtual environment

```
conda create -f environment.yml
```

After that you can activate the environment using:

```
conda activate popumapi
```

Inside the env, run the flask app:

```
flask run
```

# Limitations

- The computation is still single threaded, using Gunicorn with workers equal to the amount of processors should definitely help.
  Before that though, I should look for a different implementation for the map.
  The map grows big and is copied for each unicorn worker. Better would be to add a database for this task.
- Aggregating rasters is very CPU intensive.
  I hoped Rasterio would generate some vector instructions and/or utilize the GPU but I'm not seeing any of that on my laptop.
- I've only implemented a very specific GeoTiff format based on data from [worldpop.org](worldpop.org).
  Work needs to be done to support higher (and lower) resolution maps and different coordinate systems. This would:
  - Yield better approximations
  - Support a bigger range of radius
  - Choosing which raster to use will be more interesting

# Background

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
