# Databricks Runtime Config

## Working Version
v1.0.0-databricks-working

## Environment
DEV

## Country / Geography
- Country: USA
- Geo level: state

## States
PA, NJ, NY, CA, TX, FL

## Years
2024, 2025, 2026

## Tables
- default.usaspending_state_quarter_silver
- default.usaspending_state_quarter_gold
- default.usaspending_state_year_gold
- default.usaspending_observability_refresh_log
- default.usaspending_observability_freshness
- default.usaspending_observability_quality

## Refresh Order
1. Config cell
2. Silver ingestion cell
3. Gold aggregation cell
4. Observability metrics cell
5. SQL validation cells
6. Dashboard refresh
