# USAspending Enterprise AI Data Product

Enterprise-style open-data analytics platform for USAspending federal project spend by U.S. state and quarter.

Flask + PySpark/SparkSQL + Medallion Architecture + metadata-driven public API ingestion + interactive dashboards + RAG/agent scaffolding.

Primary public source: USAspending.gov API. API endpoints currently do not require authorization and are public DATA Act spending data.

## Capabilities

- USAspending API ingestion
- Bronze, Silver, Gold Medallion Architecture
- PySpark and SparkSQL transformations
- Local Flask dashboard
- Interactive charts and drill-down views
- Metadata-driven connector structure
- Agentic AI / RAG / MCP extension scaffolding
- GitHub Actions CI-ready structure
- Databricks migration-ready Lakehouse design

## Architecture

```text
USAspending API
  -> Bronze JSON Landing
  -> Silver Canonical State-Quarter Dataset
  -> Gold Aggregates
  -> Flask Dashboard / Charts / Reports
  -> Future: Delta Lake + Databricks SQL Dashboards

## Quick Start - Windows PowerShell

```powershell
cd usaspending_enterprise_ai_solution
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\run_local.py --start-year 2024 --end-year 2025 --states PA NJ NY CA TX
python app\flask_app.py
```

Open http://127.0.0.1:5000

## Run PySpark Medallion Pipeline

```powershell
python src\pipelines\usaspending_medallion_pipeline.py --start-year 2024 --end-year 2025 --states PA NJ NY CA TX
```

Outputs:
- `data/bronze/usaspending_spending_over_time/` raw API JSON
- `data/silver/state_quarter_spend/` normalized Parquet/CSV
- `data/gold/state_year_summary/` aggregated report views
- `data/gold/state_quarter_summary/` dashboard-ready view

## Flask Capabilities

- Interactive Plotly charts
- Drill-down table by state, year, quarter
- Metadata browser
- Workflow designer placeholder for connector + transform orchestration
- RAG/Agent page for natural-language query scaffolding

## Enterprise Extension Points

- Replace local file metadata with PostgreSQL, Snowflake, Databricks, or SQL Server
- Replace local vector index placeholder with Chroma, FAISS, pgvector, Azure AI Search, or OpenSearch
- Deploy Spark on Databricks, EMR, Synapse, or local standalone Spark
- Expose MCP server endpoints for tool-based AI orchestration

## Data Model

See `docs/DATA_MODEL.md` and `docs/MEDALLION_ARCHITECTURE.md`.
