"""
Schemas for project
"""
from pyspark.sql import types as t

all_pokemon_schema = t.StructType(
    [
        t.StructField("count", t.IntegerType(), False),
        t.StructField("next", t.StringType(), True),
        t.StructField("previous", t.StringType(), True),
        t.StructField(
            "results",
            t.ArrayType(
                t.StructType(
                    [
                        t.StructField("name", t.StringType(), False),
                        t.StructField("url", t.StringType(), False),
                    ]
                )
            ),
        ),
    ]
)

detailed_pokemon_schema = t.StructType(
    [
        t.StructField("id", t.IntegerType(), False),
        t.StructField("name", t.StringType(), False),
        t.StructField("base_experience", t.StringType(), False),
        t.StructField("weight", t.IntegerType(), False),
        t.StructField("height", t.StringType(), False),
        t.StructField("order", t.StringType(), False),
        t.StructField(
            "types",
            t.ArrayType(
                t.StructType(
                    [
                        t.StructField("slot", t.IntegerType(), False),
                        t.StructField(
                            "type",
                            t.StructType(
                                [
                                    t.StructField("name", t.StringType(), False),
                                ]
                            ),
                        ),
                    ]
                )
            ),
        ),
        t.StructField(
            "sprites",
            t.StructType([
                t.StructField("front_default", t.StringType(), False)
            ]),
        ),
        t.StructField(
            "game_indices",
            t.ArrayType(
                t.StructType([
                    t.StructField("game_index", t.IntegerType(), False),
                    t.StructField(
                        "version",
                        t.StructType([
                                t.StructField("name", t.StringType(), False),
                                t.StructField("url", t.StringType(), False)
                        ]),
                    ),
                ])
            ),
        ),
    ]
)
