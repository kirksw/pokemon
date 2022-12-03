"""
Tests for pyspark processing logic
"""

from pathlib import Path
from pokemon.schemas import all_pokemon_schema, detailed_pokemon_schema
from pyspark.sql import SparkSession
from pyspark.sql import functions as f


def test_process_all(spark: SparkSession, all_file: Path):
    """Test parsing list of all pokemon"""
    df_all = spark.read.schema(all_pokemon_schema).json(str(all_file))
    df_pokemon = df_all.select(f.explode("results.*"))
    assert df_pokemon.columns == ["name", "url"]
