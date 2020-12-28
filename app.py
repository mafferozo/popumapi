""" Popumapi App Example"""
from flask import Flask
from flask import request
from popumapi import location
from popumapi.populationmap import GeoTiffMap
from popumapi.population import Population


def setup_location_map():
    m = dict()
    location.add_file_to_map(m, "data/NL/NL.txt")
    location.add_file_to_map(m, "data/DE/DE.txt")
    location.add_file_to_map(m, "data/FR/FR.txt")
    # location.add_file_to_map(m, "data/IT/IT.txt")
    # location.add_file_to_map(m, "data/JP/JP.txt")
    # location.add_file_to_map(m, "data/ZA/ZA.txt")
    return m


def setup_population_maps():
    nl = GeoTiffMap("data/NL/nld_ppp_2020_constrained.tif")
    de = GeoTiffMap("data/DE/deu_ppp_2020_constrained.tif")
    fr = GeoTiffMap("data/FR/fra_ppp_2020_constrained.tif")
    # it = GeoTiffMap("data/IT/ita_ppp_2020_constrained.tif")
    # jp = GeoTiffMap("data/JP/jpn_ppp_2020_constrained.tif")
    # za = GeoTiffMap("data/ZA/zaf_ppp_2020_constrained.tif")
    return [nl, de, fr]


app = Flask(__name__)
loc_map = setup_location_map()
pop_maps = setup_population_maps()
popumapi_handler = Population(loc_map, pop_maps)


@app.route("/population")
def get_population():
    loc = request.args.get("location")
    radius = request.args.get("radius")
    if not (loc or radius):
        return "Usage: ?location={}&radius={}"

    pop = popumapi_handler.compute_population(loc, int(radius))

    return {"location": loc, "radius": f"{radius} km", "response": pop}
