"""
Pyspark processing logic
"""
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
from pokemon.schemas import detailed_pokemon_schema


def load_pokemon(spark: SparkSession, pokemon_path: str) -> DataFrame:
    return spark.read \
        .format("json") \
        .option("multiline", "true") \
        .schema(detailed_pokemon_schema) \
        .load(pokemon_path)


def parse_games(df: DataFrame, games=["red", "blue", "leafgreen", "white"]):
    """filter for only pokemon that are specified in the game list"""
    group_cols = ["id", "name", "base_experience", "weight", "height", "order", "types", "sprites"]
    return df \
        .withColumn("games", f.explode("game_indices.version.name")) \
        .filter(f.col("games").isin(games)) \
        .groupBy(*group_cols) \
        .agg(f.collect_list("games").alias("games"))


def parse_types(df: DataFrame):
    """parse types into a mapping"""
    df_join = df \
        .withColumn("types", f.explode("types")) \
        .withColumn("type_slot", f.concat(f.lit("type_slot_"), f.col("types.slot"))) \
        .withColumn("type_name", f.col("types.type.name")) \
        .groupBy("name").pivot("type_slot").agg(f.first("type_name"))

    return df.join(df_join, on="name").drop("types")


def parse_sprite(df: DataFrame):
    """parse front_default sprite to be used a sprite"""
    return df \
        .withColumn("sprite", f.col("sprites.front_default")) \
        .drop("sprites")


def calculate_bmi(df: DataFrame):
    """calculates pokemon bmi (weight / height^2)"""
    return df.withColumn("bmi", f.col("weight") / f.pow(f.col("height"), f.lit(2)))


def capitalize_name(df: DataFrame):
    """capitalizes first letter of pokemon name"""
    capitalize_first = f.udf(lambda x: str.capitalize(x))
    return df.withColumn("name", capitalize_first("name"))


if __name__ == "__main__":
    """sample code"""
    ss = SparkSession.builder.master("local[*]").appName("pokemon").getOrCreate()
    
    df_poke = load_pokemon(ss, "data/raw/pokemon/*.json") \
        .transform(parse_games) \
        .transform(parse_sprite) \
        .transform(parse_types) \
        .transform(calculate_bmi) \
        .transform(capitalize_name)

    df_poke.write.mode("overwrite").format("parquet").save("data/str/pokemon")
