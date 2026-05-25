# Databricks Setup Guide
## USASpending Enterprise AI Medallion Solution

## Purpose
Explains how to set up Databricks Free Edition or workspace execution for the USASpending Medallion notebook and dashboard.

## Import GitHub Repository
```text
Workspace -> Create -> Git folder / Repo
```
Repo:
```text
https://github.com/ajaytester007/usaspending_enterprise_ai_solution
```

## Notebook Cell Order
1. Config cell
2. Imports and API setup
3. Bronze/Silver ingestion
4. Gold aggregations
5. Observability metrics
6. SQL validation
7. Dashboard dataset validation

## Config Cell
```python
states = ["PA", "NJ", "NY", "CA", "TX", "FL"]
years = [2024, 2025, 2026]

pipeline_name = "usaspending_medallion_databricks"
source_system = "USAspending API"
refresh_mode = "FULL"
environment = "DEV"
```

## Tables
Silver:
```text
default.usaspending_state_quarter_silver
```
Gold:
```text
default.usaspending_state_quarter_gold
default.usaspending_state_year_gold
```
Observability:
```text
default.usaspending_observability_refresh_log
default.usaspending_observability_freshness
default.usaspending_observability_quality
```

## Refresh Process
1. Update config.
2. Run config.
3. Run ingestion.
4. Run Gold.
5. Run observability.
6. Refresh dashboard datasets.
7. Refresh dashboard canvas.

## Validation
```sql
SELECT DISTINCT state FROM default.usaspending_state_quarter_gold ORDER BY state;
```

```sql
SELECT DISTINCT year FROM default.usaspending_state_quarter_gold ORDER BY year;
```
