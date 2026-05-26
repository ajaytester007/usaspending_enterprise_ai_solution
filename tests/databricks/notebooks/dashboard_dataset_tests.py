# Databricks notebook source

datasets = {
    "quarter_gold": """
        SELECT *
        FROM default.usaspending_state_quarter_gold
    """,
    "year_gold": """
        SELECT *
        FROM default.usaspending_state_year_gold
    """,
    "refresh_log": """
        SELECT *
        FROM default.usaspending_observability_refresh_log
    """,
    "quality_metrics": """
        SELECT *
        FROM default.usaspending_observability_quality
    """,
    "geo_readiness_summary": """
        SELECT
          country,
          country_code,
          geo_level,
          COUNT(DISTINCT state) AS geography_count,
          COUNT(DISTINCT period) AS period_count,
          SUM(total_obligations) AS total_obligations,
          SUM(transaction_count) AS transaction_count
        FROM default.usaspending_state_quarter_gold
        GROUP BY country, country_code, geo_level
    """,
    "qoq_growth": """
        WITH ordered_quarters AS (
          SELECT
            state,
            period,
            year,
            quarter,
            total_obligations,
            LAG(total_obligations) OVER (
              PARTITION BY state
              ORDER BY year, quarter
            ) AS prev_quarter_obligations
          FROM default.usaspending_state_quarter_gold
        )
        SELECT *
        FROM ordered_quarters
        WHERE prev_quarter_obligations IS NOT NULL
    """,
    "yoy_growth": """
        SELECT
          curr.state,
          curr.quarter,
          curr.year AS current_year,
          curr.total_obligations AS current_obligations,
          prev.total_obligations AS previous_obligations
        FROM default.usaspending_state_quarter_gold curr
        LEFT JOIN default.usaspending_state_quarter_gold prev
          ON curr.state = prev.state
         AND curr.quarter = prev.quarter
         AND curr.year = prev.year + 1
        WHERE prev.total_obligations IS NOT NULL
    """,
}

for name, sql in datasets.items():
    df = spark.sql(sql)
    row_count = df.count()
    assert row_count > 0, f"Dashboard dataset returned zero rows: {name}"
    print(f"PASS: {name} returned {row_count} rows")

print("PASS: Dashboard dataset tests completed successfully.")