import shutil
import time
import pandas as pd
import argparse
import json
from pathlib import Path
from typing import List
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

from src.connectors.usaspending_client import fetch_range

ALL_STATES = "AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split()


def build_spark() -> SparkSession:
    import os
    from pyspark.sql import SparkSession

    venv_python = os.path.abspath(".venv/Scripts/python.exe")

    os.environ["PYSPARK_PYTHON"] = venv_python
    os.environ["PYSPARK_DRIVER_PYTHON"] = venv_python
    os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

    return (
        SparkSession.builder
        .appName("USASpendingMedallionPipeline")
        .master("local[1]")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.python.worker.reuse", "false")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.hadoop.io.native.lib.available", "false")
        .config("spark.hadoop.fs.file.impl.disable.cache", "true")
        .config(
            "spark.driver.extraJavaOptions",
            "-Dorg.apache.hadoop.util.NativeCodeLoader.disable=true"
        )
        .config(
            "spark.cleaner.referenceTracking.cleanCheckpoints",
            "true"
        )
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")
    return spark


def bronze_to_silver(spark: SparkSession, bronze_dir: str, silver_dir: str) -> None:
    rows = []
    for file in Path(bronze_dir).glob("state=*_year=*_quarter=*.json"):
        payload = json.loads(file.read_text(encoding="utf-8"))
        results = payload.get("response", {}).get("results", [])
        total_amount = 0.0
        tx_count = 0
        for item in results:
            total_amount += float(item.get("aggregated_amount", 0) or 0)
            tx_count += int(item.get("transaction_count", 0) or 0)
        rows.append((
            payload.get("source"), payload.get("state"), int(payload.get("year")), payload.get("quarter"),
            payload.get("period_start"), payload.get("period_end"), total_amount, tx_count, str(file)
        ))

    schema = StructType([
        StructField("source", StringType(), True),
        StructField("state", StringType(), False),
        StructField("year", IntegerType(), False),
        StructField("quarter", StringType(), False),
        StructField("period_start", StringType(), True),
        StructField("period_end", StringType(), True),
        StructField("total_obligations", DoubleType(), True),
        StructField("transaction_count", IntegerType(), True),
        StructField("raw_file", StringType(), True),
    ])
    df = spark.createDataFrame(rows, schema)
    df = df.withColumn("period", F.concat_ws("-", F.col("year"), F.col("quarter")))

    Path("data/silver").mkdir(parents=True, exist_ok=True)

    df.toPandas().to_csv(f"{silver_dir}.csv", index=False)
    df.toPandas().to_csv("data/silver/state_quarter_spend.csv", index=False)


def silver_to_gold(spark: SparkSession, silver_dir: str, gold_dir: str) -> None:
    
    import pandas as pd
    
    df = spark.createDataFrame(
       pd.read_csv(f"{silver_dir}.csv")
    )

    df.createOrReplaceTempView("state_quarter_spend")

    quarter_summary = spark.sql("""
        SELECT state, year, quarter, period,
               SUM(total_obligations) AS total_obligations,
               SUM(transaction_count) AS transaction_count
        FROM state_quarter_spend
        GROUP BY state, year, quarter, period
    """)

    year_summary = spark.sql("""
        SELECT state, year,
               SUM(total_obligations) AS total_obligations,
               SUM(transaction_count) AS transaction_count,
               COUNT(*) AS quarters_reported
        FROM state_quarter_spend
        GROUP BY state, year
    """)


    from pathlib import Path
    import pandas as pd

    Path(gold_dir).mkdir(parents=True, exist_ok=True)

    quarter_pdf = quarter_summary.toPandas()
    year_pdf = year_summary.toPandas()

    # CSV outputs
    quarter_pdf.to_csv(
        f"{gold_dir}/state_quarter_summary.csv",
        index=False
    )

    year_pdf.to_csv(
        f"{gold_dir}/state_year_summary.csv",
        index=False
    )

    # Parquet outputs via pandas instead of Spark/Hadoop
    quarter_pdf.to_parquet(
        f"{gold_dir}/state_quarter_summary.parquet",
        index=False
    )

    year_pdf.to_parquet(
        f"{gold_dir}/state_year_summary.parquet",
        index=False
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-year", type=int, default=2024)
    parser.add_argument("--end-year", type=int, default=2025)
    parser.add_argument("--states", nargs="+", default=["PA", "NJ", "NY", "CA", "TX"])
    args = parser.parse_args()

    bronze = "data/bronze/usaspending_spending_over_time"
    silver = "data/silver/state_quarter_spend"
    gold = "data/gold"

    states: List[str] = args.states if args.states != ["ALL"] else ALL_STATES
    fetch_range(states, args.start_year, args.end_year, bronze)
    spark = build_spark()
    
    try:
        bronze_to_silver(spark, bronze, silver)
        silver_to_gold(spark, silver, gold)
        print("Medallion pipeline complete.")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
