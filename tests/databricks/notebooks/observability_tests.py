# Databricks notebook source
from pyspark.sql import functions as F

REFRESH_LOG = "default.usaspending_observability_refresh_log"
QUALITY = "default.usaspending_observability_quality"

assert spark.catalog.tableExists(REFRESH_LOG), f"Missing table: {REFRESH_LOG}"
assert spark.catalog.tableExists(QUALITY), f"Missing table: {QUALITY}"

refresh_df = spark.table(REFRESH_LOG)
quality_df = spark.table(QUALITY)

assert refresh_df.count() > 0, "Refresh log is empty"
assert quality_df.count() > 0, "Quality metrics table is empty"

required_refresh_cols = [
    "pipeline_name",
    "refresh_timestamp_utc",
    "source",
    "states_requested",
    "years_requested",
    "row_count_silver",
    "row_count_gold_quarter",
    "row_count_gold_year",
    "status",
]

missing_refresh_cols = [c for c in required_refresh_cols if c not in refresh_df.columns]
assert not missing_refresh_cols, f"Missing refresh log columns: {missing_refresh_cols}"

latest_refresh = (
    refresh_df
    .orderBy(F.col("refresh_timestamp_utc").desc())
    .limit(1)
    .collect()[0]
)

assert latest_refresh["status"] == "SUCCESS", "Latest refresh did not complete successfully"
assert latest_refresh["row_count_silver"] > 0, "Latest Silver row count is zero"
assert latest_refresh["row_count_gold_quarter"] > 0, "Latest Gold quarter row count is zero"
assert latest_refresh["row_count_gold_year"] > 0, "Latest Gold year row count is zero"

quality_metrics = [row["metric_name"] for row in quality_df.select("metric_name").distinct().collect()]

expected_metrics = [
    "silver_null_state_count",
    "silver_null_period_count",
    "silver_negative_obligations_count",
    "gold_quarter_row_count",
]

missing_metrics = [m for m in expected_metrics if m not in quality_metrics]
assert not missing_metrics, f"Missing quality metrics: {missing_metrics}"

print("PASS: Observability tests completed successfully.")