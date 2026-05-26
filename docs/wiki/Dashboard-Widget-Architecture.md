# Dashboard Widget Architecture

## Purpose
This page documents the dashboard widget model for the USASpending Enterprise AI Medallion Solution.

## Dashboard Page Inventory

| Page | Purpose |
|---|---|
| Executive Overview | Executive KPIs and high-level spend intelligence |
| Geography Drilldown | Geographic analytics and geo-readiness |
| Quarterly Trends | Time-series spending analytics |
| Data Quality | Data quality and validation telemetry |
| Observability | Pipeline refresh and operational metrics |
| Advanced Analytics | Growth, concentration, ranking, and trend analytics |
| Global Filters | Cross-dashboard filter controls |

## Widget Categories

### KPI Widgets
Used for executive metrics:
- Total Obligations
- Transactions
- Countries
- States
- Periods

### Trend Widgets
Used for temporal analysis:
- Quarterly Federal Obligations by State
- Obligations by Period
- Spending Trend Over Time
- QoQ Growth
- YoY Growth

### Geography Widgets
Used for geographic analysis:
- Total Obligations by Geography
- Geography Readiness Summary
- State-Quarter Detail

### Quality and Observability Widgets
Used for operational governance:
- Pipeline Refresh Log
- Quality Metrics
- Data Freshness
- Known Issue tracking

### Advanced Analytics Widgets
Used for exploratory analytics:
- Top 10 States
- Spending Concentration
- State Performance Ranking
- State-Quarter Heatmap
- Transaction Volume vs Value
- Period-to-Period Comparison

## Widget Governance Standards

Each widget should have:
- meaningful title
- source dataset identified
- clear measure definition
- filter compatibility
- documented purpose
- known limitations if any

## Naming Convention

Recommended:

```text
kpi_<metric_name>
line_<metric_name>
bar_<dimension>_<metric>
table_<subject>
filter_<field>
```

Examples:

```text
kpi_total_obligations
line_period_obligations
bar_state_obligations
table_quarter_detail
filter_country
```

## Future Enhancements
- widget regression tests
- dashboard certification workflow
- widget-level lineage mapping
- AI-generated dashboard summaries
