# v1.2.0-enterprise-dashboard-analytics

## Release Title
Enterprise Dashboard Analytics Baseline

## Release Summary
This release promotes the Databricks-side dashboard enhancements, semantic dataset layer, observability model, quality metrics, geo-readiness foundation, and advanced analytics widgets into the Git-governed solution baseline.

The platform has now evolved from a Databricks medallion proof-of-concept into an Enterprise Spend Intelligence Platform with operational dashboards, analytical governance, extensible geography fields, and future-ready AI/GIS/multi-country architecture.

---

## Major Features Added

### 1. Executive Dashboard Enhancements
Added and published executive dashboard pages:
- Executive Overview
- Geography Drilldown
- Quarterly Trends
- Data Quality
- Observability
- Advanced Analytics
- Global Filters

### 2. Global Filter Architecture
Implemented dashboard filters for:
- country
- geo_level
- state
- year
- quarter
- period

These filters establish the foundation for multi-country and multi-geography drilldowns.

### 3. Semantic Dashboard Dataset Layer
Introduced reusable SQL datasets:
- quarter_gold
- year_gold
- refresh_log
- quality_metrics
- geo_readiness_summary
- top_10_states
- state_performance_ranking
- spending_concentration
- yoy_growth
- qoq_growth

### 4. Advanced Analytics
Added advanced analytics capabilities:
- QoQ growth analytics
- YoY growth analytics
- Top state analysis
- Spending concentration analysis
- State ranking analytics
- Heatmap-style analytical tables
- Trend analytics
- Scatter analytics foundation
- Forecast readiness

### 5. Observability
Added observability architecture:
- refresh log
- quality metrics
- operational telemetry
- pipeline health dashboard
- refresh auditability

### 6. Data Quality Governance
Added data quality governance and known issue tracking:
- Known issue KI-001 for transaction_count = 0
- data quality runbooks
- observability quality framework
- issue register
- telemetry model

### 7. Geo Readiness
Added geographic readiness architecture:
- country
- country_code
- geo_level
- state-level baseline
- future-ready GIS roadmap

### 8. Documentation and Wiki Expansion
Added/updated:
- runbooks
- ADRs
- dashboard governance
- observability docs
- known issues
- GIS roadmap
- multi-country roadmap
- release management guidance

---

## Known Issues

### KI-001: transaction_count = 0
Transaction-based widgets are currently degraded until the ingestion logic is updated to retrieve the correct transaction/award count from source APIs.

Affected:
- Transactions KPI
- Average Transaction Size
- Transaction Volume vs Value Scatter
- State Performance Ranking transaction metrics

Current mitigation:
- use obligation-based analytics for executive interpretation.

---

## Architecture Positioning
This release positions the platform as:

- Databricks Lakehouse reference implementation
- Enterprise CFO spend analytics platform
- Federal expenditure intelligence system
- Geospatial public sector analytics foundation
- Operational intelligence and observability platform
- AI-ready semantic analytics framework

---

## Suggested Git Tag

```text
v1.2.0-enterprise-dashboard-analytics
```

## Suggested GitHub Release Title

```text
v1.2.0 - Enterprise Dashboard Analytics
```
