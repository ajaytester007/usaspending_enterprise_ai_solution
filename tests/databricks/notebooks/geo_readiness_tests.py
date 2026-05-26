# Databricks notebook source
from pyspark.sql import functions as F

GOLD_QUARTER = "default.usaspending_state_quarter_gold"

assert spark.catalog.tableExists(GOLD_QUARTER), f"Missing table: {GOLD_QUARTER}"

df = spark.table(GOLD_QUARTER)

required_geo_columns = [
    "country",
    "country_code",
    "geo_level",
    "state",
]

missing_geo_columns = [c for c in required_geo_columns if c not in df.columns]
assert not missing_geo_columns, f"Missing geo columns: {missing_geo_columns}"

country_values = [r["country"] for r in df.select("country").distinct().collect()]
country_code_values = [r["country_code"] for r in df.select("country_code").distinct().collect()]
geo_level_values = [r["geo_level"] for r in df.select("geo_level").distinct().collect()]

assert "USA" in country_values, "USA not found in country values"
assert "US" in country_code_values, "US not found in country_code values"
assert "state" in geo_level_values, "state not found in geo_level values"

expected_states = ["PA", "NJ", "NY", "CA", "TX", "FL"]
actual_states = [r["state"] for r in df.select("state").distinct().collect()]

missing_states = sorted(set(expected_states) - set(actual_states))
assert not missing_states, f"Missing expected states: {missing_states}"

invalid_compound_states = df.filter(F.col("state").contains(",")).count()
assert invalid_compound_states == 0, "Compound state values found, e.g., 'TX, FL'"

geo_summary = (
    df.groupBy("country", "country_code", "geo_level")
    .agg(
        F.countDistinct("state").alias("geography_count"),
        F.countDistinct("period").alias("period_count"),
        F.sum("total_obligations").alias("total_obligations"),
    )
)

summary_row = geo_summary.collect()[0]

assert summary_row["geography_count"] >= 6, "Expected at least 6 states"
assert summary_row["period_count"] >= 12, "Expected at least 12 periods"
assert summary_row["total_obligations"] > 0, "Total obligations should be greater than zero"

display(geo_summary)

print("PASS: Geo readiness tests completed successfully.")