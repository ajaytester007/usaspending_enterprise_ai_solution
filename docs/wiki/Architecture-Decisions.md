# Architecture Decisions
## USASpending Enterprise AI Medallion Solution

## Purpose
Captures key architecture decisions and rationale.

## Decisions

### Medallion Architecture
Use Bronze, Silver, and Gold layers for raw preservation, normalized data, and analytics-ready aggregates.

### USAspending as Initial Source
Start with USA federal spending because it provides public API-based data suitable for repeatable analytics.

### Databricks for Managed Spark
Databricks avoids local Windows Spark friction and provides managed Spark, Delta tables, SQL, and dashboard support.

### Delta Tables
Persist Silver and Gold as Delta tables to support reliable Lakehouse analytics.

### Notebook and Dashboard Separation
Version-control notebook source, SQL, screenshots, and dashboard runbooks separately.

### Central Config Cell
All runtime variables such as states, years, source system, and environment should live in the top config cell.

### Observability Layer
Create refresh, freshness, and quality tables for operational monitoring.

### Multi-Country Roadmap
Add `country` and `geo_level` fields before expanding internationally.

## Future Direction
- GIS enrichment
- country connector registry
- Delta Live Tables
- Databricks Jobs
- Unity Catalog
- Lakehouse Monitoring
- Databricks Asset Bundles
- RAG over metadata and runbooks
- MCP server integration
