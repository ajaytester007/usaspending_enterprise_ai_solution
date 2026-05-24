# Agentic AI, RAG, MCP and Multi-Agent Blueprint

## Agent Roles

1. Data Acquisition Agent
   - Reads connector metadata
   - Invokes API fetchers
   - Writes Bronze payloads

2. Data Quality Agent
   - Validates schema, freshness, nulls and anomalies
   - Produces quality reports

3. Semantic Modeling Agent
   - Explains datasets, indicators, metrics, and dimensions
   - Maintains glossary and business metadata

4. Analytics Agent
   - Converts natural language to SparkSQL or DuckDB SQL
   - Runs approved read-only queries
   - Returns charts and traceable evidence

5. Governance Agent
   - Verifies source domains, lineage, refresh status, PII risk, and audit readiness

## RAG Design

Knowledge corpus:
- `docs/*.md`
- `config/metadata_catalog.json`
- curated schema summaries
- dashboard/report definitions

Vector index options:
- local FAISS/Chroma
- pgvector
- Azure AI Search
- OpenSearch

## MCP Design

Expose tools:
- `refresh_dataset(start_year, end_year, states)`
- `query_gold_sql(sql)`
- `get_metadata_catalog()`
- `get_lineage(record_id)`
- `generate_report(view_name)`

Security:
- Read-only SQL by default
- command allowlist
- connector allowlist
- no shell execution from arbitrary user input
- audit every tool call
