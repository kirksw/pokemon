"""
Tests for pyspark parsing logic
"""

from pathlib import Path
from pokemon.schemas import all_pokemon_schema, detailed_pokemon_schema
from pyspark.sql import SparkSession
from pyspark.sql import functions as f


def test_parse_all(spark: SparkSession, all_file: Path):
    """Test parsing list of all pokemon"""
    df_all = spark.read.schema(all_pokemon_schema).json(str(all_file))
    # check the correct number of pokemon exist
    assert df_all.select(f.explode("results.name").alias("name")).count() >= 1154
    # check prev and next are null (we have all pokemon in the json)
    assert df_all.filter("previous is not NULL").count() == 0
    assert df_all.filter("next is not NULL").count() == 0


def test_parse_bulbasaur(spark: SparkSession, one_file: Path):
    """Test parsing bulbasaur json"""
    df_bulb = spark.read.schema(detailed_pokemon_schema).json(str(one_file))
    # check parsing succeeded (Nothing is optional)
    assert df_bulb.count() == 1
