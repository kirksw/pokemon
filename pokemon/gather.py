"""
Http request logic
"""

import requests
from pyspark.sql import SparkSession, DataFrame, Row
from pyspark.sql import functions as f
from pokemon.schemas import all_pokemon_schema


PKAPI_HEADER = {"content-type": "application/json"}


class APIException(Exception):
    """Exception for failed API calls"""


def get_request(url: str, timeout=60) -> str:
    """Runs get request and returns string object"""
    res = requests.get(
        url=url,
        headers=PKAPI_HEADER,
        timeout=timeout,
    )

    if res.status_code != 200:
        raise APIException(
            f"GET Request to [{url}] failed with error code [{res.status_code}]"
        )

    return res.text


def save_json(pokemon: Row):
    """Worker job to gather a single pokemon from API"""
    name = pokemon[0].name
    gather_one(name, f"data/raw/pokemon/{name}.json")


def gather_one(pokemon_id: int, out_fn: str):
    """Retrieve detailed data for a single pokemon"""
    if id is None:
        raise ValueError("Must supply a valid id parameter")

    res_text = get_request(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")

    with open(out_fn, "w", encoding="utf-8") as file_handle:
        file_handle.write(res_text)

    return out_fn


def gather_overview(out_fn: str):
    """Retrieve basic data for all pokemon"""
    res_text = get_request("https://pokeapi.co/api/v2/pokemon?limit=10000&offset=0")

    with open(out_fn, "w", encoding="utf-8") as file_handle:
        file_handle.write(res_text)

    return out_fn


def gather_all(df_all: DataFrame):
    """
    Typically would use an async data producer to write data for autoloader / kafka
    to read as a stream, however for this POC will just farm to workers to save
    files for the next stage
    """
    df_pk = df_all.select(f.explode("results")).repartition(10)
    df_pk.foreach(save_json)


if __name__ == "__main__":
    """sample code"""
    # code to test spark pulling in all the json files
    ss = SparkSession.builder.master("local[*]").appName("pokemon").getOrCreate()

    fn_all = gather_overview("data/raw/all_pokemon.json")
    df_all = ss.read.format("json").schema(all_pokemon_schema).load(fn_all)
    gather_all(df_all)

    # code to test indiviual functions
    BULBASAUR_ID = 1
    gather_overview("data/raw/all_pokemon.json")
    gather_one(BULBASAUR_ID, "data/raw/bulbasaur.json")
