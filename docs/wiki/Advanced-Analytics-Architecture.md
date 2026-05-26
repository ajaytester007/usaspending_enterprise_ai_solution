# Advanced Analytics Architecture

## Purpose
Documents the advanced analytics model for the Databricks dashboard.

## Current Analytical Capabilities
- Top 10 states by obligations
- Spending concentration analysis
- YoY growth
- QoQ growth
- State ranking
- State-quarter heatmap table
- Transaction volume vs value scatter
- Period comparison
- Spending trend analysis

## Analytical Dataset Layer
Advanced analytics datasets are implemented as Databricks SQL datasets and should also be saved under:

```text
sql/analytics/
```

## Current Limitations
KI-001 causes transaction_count to equal zero, which impacts transaction-volume and average-transaction-size calculations.

## Future Enhancements
- ARIMA forecasting
- Prophet forecasting
- Spark ML forecasting
- Databricks AutoML
- anomaly detection
- state clustering
- executive narrative generation
