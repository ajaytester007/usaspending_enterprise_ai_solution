# Databricks notebook source
# =========================================================
# USAspending Enterprise Medallion Config
# =========================================================

states = ["PA", "NJ", "NY", "CA", "TX", "FL"]

years = [2024, 2025, 2026]

quarters = {
    "Q1": ("01-01", "03-31"),
    "Q2": ("04-01", "06-30"),
    "Q3": ("07-01", "09-30"),
    "Q4": ("10-01", "12-31"),
}

pipeline_name = "usaspending_medallion_databricks"

source_system = "USAspending API"

refresh_mode = "FULL"

environment = "DEV"

# COMMAND ----------

expected_states = ["PA","NJ","NY","CA","TX","FL"]

invalid_states = silver_df.filter(
    ~F.col("state").isin(expected_states)
)

display(invalid_states)

# COMMAND ----------

print(states)
print(years)
print (quarters)

# COMMAND ----------

import requests
import pandas as pd
from pyspark.sql import functions as F

endpoint = "https://api.usaspending.gov/api/v2/search/spending_over_time/"

rows = []

for year in years:
    for quarter, dates in quarters.items():
        for state in states:
              body = {
                "group": "quarter",
                "subawards": False,
                "filters": {
                    "time_period": [{
                        "start_date": f"{year}-{dates[0]}",
                        "end_date": f"{year}-{dates[1]}"
                    }],
                    "place_of_performance_scope": "domestic",
                    "place_of_performance_locations": [
                        {"country": "USA", "state": state}
                    ],
                    "award_type_codes": ["A", "B", "C", "D", "02", "03", "04", "05"]
                }
            }

import time

rows = []

for year in years:
    for quarter, dates in quarters.items():
        for state in states:

            body = {
                "group": "quarter",
                "subawards": False,
                "filters": {
                    "time_period": [{
                        "start_date": f"{year}-{dates[0]}",
                        "end_date": f"{year}-{dates[1]}"
                    }],
                    "place_of_performance_scope": "domestic",
                    "place_of_performance_locations": [
                        {"country": "USA", "state": state}
                    ],
                    "award_type_codes": ["A", "B", "C", "D", "02", "03", "04", "05"]
                }
            }

            success = False

            for attempt in range(3):

                try:
                    r = requests.post(endpoint, json=body, timeout=120)

                    if r.status_code == 200:
                        payload = r.json()
                        success = True
                        time.sleep(1)
                        break

                    print(f"Retry {attempt+1}: HTTP {r.status_code}")

                except Exception as e:
                    print(f"Retry {attempt+1} failed: {e}")

                time.sleep(5)

            if not success:
                print(f"Skipping {state} {year} {quarter}")
                continue

            total = sum(
                float(x.get("aggregated_amount", 0) or 0)
                for x in payload.get("results", [])
            )

            count = sum(
                int(x.get("transaction_count", 0) or 0)
                for x in payload.get("results", [])
            )

            rows.append({
                "state": state,
                "year": year,
                "quarter": quarter,
                "period": f"{year}-{quarter}",
                "total_obligations": total,
                "transaction_count": count
            })

silver_df = spark.createDataFrame(pd.DataFrame(rows))

silver_df.write.format("delta").mode("overwrite").saveAsTable(
    "default.usaspending_state_quarter_silver"
)

display(silver_df)

# COMMAND ----------

gold_quarter = (
    silver_df
    .groupBy("state", "year", "quarter", "period")
    .agg(
        F.sum("total_obligations").alias("total_obligations"),
        F.sum("transaction_count").alias("transaction_count")
    )
)

gold_year = (
    silver_df
    .groupBy("state", "year")
    .agg(
        F.sum("total_obligations").alias("total_obligations"),
        F.sum("transaction_count").alias("transaction_count"),
        F.countDistinct("quarter").alias("quarters_reported")
    )
)

gold_quarter.write.format("delta").mode("overwrite").saveAsTable(
    "default.usaspending_state_quarter_gold"
)

gold_year.write.format("delta").mode("overwrite").saveAsTable(
    "default.usaspending_state_year_gold"
)

display(gold_quarter)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT state, year, quarter, total_obligations
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC ORDER BY year, quarter, state;

# COMMAND ----------

gold_quarter = (
    silver_df
    .groupBy("state", "year", "quarter", "period")
    .agg(
        F.sum("total_obligations").alias("total_obligations"),
        F.sum("transaction_count").alias("transaction_count")
    )
)

gold_year = (
    silver_df
    .groupBy("state", "year")
    .agg(
        F.sum("total_obligations").alias("total_obligations"),
        F.sum("transaction_count").alias("transaction_count"),
        F.countDistinct("quarter").alias("quarters_reported")
    )
)

gold_quarter.write.format("delta").mode("overwrite").saveAsTable(
    "default.usaspending_state_quarter_gold"
)

gold_year.write.format("delta").mode("overwrite").saveAsTable(
    "default.usaspending_state_year_gold"
)

display(gold_quarter)

# COMMAND ----------

from pyspark.sql import functions as F
from datetime import datetime

from datetime import datetime, timezone

refresh_ts = datetime.now(timezone.utc).isoformat()

observability_refresh = spark.createDataFrame([
    {
        "pipeline_name": "usaspending_medallion_databricks",
        "refresh_timestamp_utc": refresh_ts,
        "source": "USAspending API",
        "states_requested": ",".join(states),
        "years_requested": ",".join([str(y) for y in years]),
        "row_count_silver": silver_df.count(),
        "row_count_gold_quarter": gold_quarter.count(),
        "row_count_gold_year": gold_year.count(),
        "status": "SUCCESS"
    }
])

freshness = (
    silver_df
    .groupBy("state")
    .agg(
        F.max("year").alias("latest_year"),
        F.max("period").alias("latest_period"),
        F.count("*").alias("period_count"),
        F.sum("total_obligations").alias("total_obligations")
    )
    .withColumn("refresh_timestamp_utc", F.lit(refresh_ts))
)

quality = spark.createDataFrame([
    {
        "metric_name": "silver_null_state_count",
        "metric_value": silver_df.filter(F.col("state").isNull()).count(),
        "refresh_timestamp_utc": refresh_ts
    },
    {
        "metric_name": "silver_null_period_count",
        "metric_value": silver_df.filter(F.col("period").isNull()).count(),
        "refresh_timestamp_utc": refresh_ts
    },
    {
        "metric_name": "silver_negative_obligations_count",
        "metric_value": silver_df.filter(F.col("total_obligations") < 0).count(),
        "refresh_timestamp_utc": refresh_ts
    },
    {
        "metric_name": "gold_quarter_row_count",
        "metric_value": gold_quarter.count(),
        "refresh_timestamp_utc": refresh_ts
    }
])

observability_refresh.write.format("delta").mode("append").saveAsTable(
    "default.usaspending_observability_refresh_log"
)

freshness.write.format("delta").mode("overwrite").saveAsTable(
    "default.usaspending_observability_freshness"
)

quality.write.format("delta").mode("append").saveAsTable(
    "default.usaspending_observability_quality"
)

display(observability_refresh)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM default.usaspending_observability_refresh_log
# MAGIC ORDER BY refresh_timestamp_utc DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM default.usaspending_observability_quality
# MAGIC ORDER BY refresh_timestamp_utc DESC, metric_name;