# Semantic Dataset Model

## Purpose
The semantic dataset layer decouples dashboard widgets from raw Delta tables and creates reusable governed analytical datasets.

## Architecture

```text
Delta Tables
→ Semantic SQL Datasets
→ Dashboard Widgets
→ Executive Analytics
```

## Core Semantic Datasets

| Dataset | Purpose |
|---|---|
| quarter_gold | Quarter-level analytical fact dataset |
| year_gold | Year-level aggregation dataset |
| refresh_log | Pipeline observability dataset |
| quality_metrics | Data quality telemetry dataset |
| geo_readiness_summary | Geography readiness dataset |
| top_10_states | Executive ranking dataset |
| spending_concentration | Pareto/concentration analytics |
| yoy_growth | Year-over-year analytics |
| qoq_growth | Quarter-over-quarter analytics |
| state_performance_ranking | Multi-metric state ranking |

## Benefits
- reusable SQL logic
- governed KPI definitions
- dashboard consistency
- simplified testing
- improved lineage
- future AI semantic layer readiness

## Dataset Governance Rules
1. Each semantic dataset must have a documented purpose.
2. Each dataset should be saved as a `.sql` artifact.
3. Each dashboard widget should reference an approved dataset.
4. Dataset changes should be version-controlled.
5. Dataset changes affecting KPI meaning require release notes.

## Future Direction
- dbt-style semantic models
- Unity Catalog table comments
- metric definitions
- AI-ready semantic catalog
- data product ownership
