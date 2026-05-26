# Databricks notebook source
from pyspark.sql import functions as F

REQUIRED_TABLES = [
    "default.usaspending_state_quarter_silver",
    "default.usaspending_state_quarter_gold",
    "default.usaspending_state_year_gold",
]

for table in REQUIRED_TABLES:
    assert spark.catalog.tableExists(table), f"Missing required table: {table}"

silver_df = spark.table("default.usaspending_state_quarter_silver")
gold_quarter_df = spark.table("default.usaspending_state_quarter_gold")
gold_year_df = spark.table("default.usaspending_state_year_gold")

assert silver_df.count() > 0, "Silver table is empty"
assert gold_quarter_df.count() > 0, "Gold quarter table is empty"
assert gold_year_df.count() > 0, "Gold year table is empty"

required_columns = [
    "country",
    "country_code",
    "geo_level",
    "state",
    "year",
    "quarter",
    "period",
    "total_obligations",
    "transaction_count",
    "source_system",
]

missing_columns = [c for c in required_columns if c not in silver_df.columns]
assert not missing_columns, f"Missing Silver columns: {missing_columns}"

null_checks = {
    "country": silver_df.filter(F.col("country").isNull()).count(),
    "country_code": silver_df.filter(F.col("country_code").isNull()).count(),
    "geo_level": silver_df.filter(F.col("geo_level").isNull()).count(),
    "state": silver_df.filter(F.col("state").isNull()).count(),
    "period": silver_df.filter(F.col("period").isNull()).count(),
}

failures = {k: v for k, v in null_checks.items() if v > 0}
assert not failures, f"Null quality failures: {failures}"

negative_obligations = silver_df.filter(F.col("total_obligations") < 0).count()
assert negative_obligations == 0, "Negative obligations found"

invalid_states = silver_df.filter(~F.col("state").isin(["PA", "NJ", "NY", "CA", "TX", "FL"])).count()
assert invalid_states == 0, "Invalid state values found"

print("PASS: Integration quality checks completed successfully.")