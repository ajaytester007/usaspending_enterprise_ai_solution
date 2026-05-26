# ADR-001: Databricks Selected as Enterprise Analytics Platform

## Status
Accepted

## Context
The solution initially began as a local PySpark + Flask analytics prototype. As the platform evolved, several operational limitations emerged:
- Windows Spark instability
- Hadoop/winutils dependency issues
- dashboard scalability limitations
- operational observability gaps
- governance limitations
- scalability constraints

The platform also required:
- managed Spark execution
- Delta Lake support
- enterprise dashboards
- semantic SQL datasets
- operational telemetry
- future ML support
- multi-country scalability

## Decision
Databricks was selected as the primary enterprise analytics and Lakehouse execution platform.

## Rationale
Databricks provides:
- managed Apache Spark
- Delta Lake integration
- SQL Warehouses
- interactive dashboards
- notebook orchestration
- observability tooling
- governance readiness
- ML and AI extensibility
- GIS integration potential

## Consequences
### Positive
- reduced operational friction
- enterprise dashboard support
- scalable Lakehouse architecture
- schema evolution support
- stronger governance alignment

### Negative
- cloud dependency introduced
- dashboard export portability varies by edition
- workspace governance complexity increased

## Future Direction
- Unity Catalog integration
- Databricks Asset Bundles
- Delta Live Tables
- ML forecasting
- Mosaic GIS integration