\# Databricks Notebook Runbook

\## USASpending Enterprise AI Medallion Solution



\---



\# Purpose



This runbook describes the operational usage of the Databricks notebook implementation for the USASpending Enterprise AI Solution.



The notebook implements a Medallion Lakehouse architecture using:



\- Bronze Layer

\- Silver Layer

\- Gold Layer

\- Observability Layer

\- Dashboard Dataset Layer



\---



\# Architecture Overview



\## Pipeline Layers



| Layer | Purpose |

|---|---|

| Bronze | Raw API ingestion |

| Silver | Cleansed normalized transactional data |

| Gold | Aggregated analytics-ready datasets |

| Observability | Refresh metrics and operational telemetry |

| Dashboard | Interactive BI visualization datasets |



\---



\# Environment Configuration



\## Runtime



Recommended Databricks Runtime:



\- 14.x LTS or higher

\- Python 3.10+



\---



\# Required Libraries



Notebook uses:



```python

import requests

import pandas as pd

from pyspark.sql import functions as F

from datetime import datetime

