"""
Test wide fixtures
"""

import pytest
from pyspark.sql import SparkSession
from pokemon.gather import gather_one, gather_overview


@pytest.fixture(scope="session", autouse=True)
def spark():
    """Use a single spark fixture for all tests"""
    return SparkSession.builder.appName("pokemon-test").getOrCreate()


@pytest.fixture(scope="session", autouse=True)
def all_file(tmp_path_factory):
    """Fixture to download all_pokemon.json file for tests"""
    out_fn = tmp_path_factory.mktemp("data") / "all_pokemon.json"
    gather_overview(out_fn)
    return out_fn


@pytest.fixture(scope="session", autouse=True)
def one_file(tmp_path_factory):
    """Fixture to download bulbasaur.json file for tests"""
    out_fn = tmp_path_factory.mktemp("data") / "bulbasaur.json"
    gather_one(1, out_fn)
    return out_fn
