# Unity Catalog Migration

## Purpose
Defines the future migration from workspace.default to governed Unity Catalog namespaces.

## Current State
The current implementation uses:

```text
workspace.default
```

## Target State

```text
enterprise_finance.analytics
enterprise_finance.observability
enterprise_finance.governance
```

## Proposed Catalog Structure

```text
enterprise_finance
  analytics
    usaspending_state_quarter_silver
    usaspending_state_quarter_gold
    usaspending_state_year_gold
  observability
    refresh_log
    quality_metrics
    freshness
  governance
    connector_registry
    issue_register
    schema_registry
```

## Benefits
- governance
- permissions
- lineage
- auditability
- table ownership
- certification

## Migration Steps
1. Create Unity Catalog catalog.
2. Create schemas.
3. Move or recreate Delta tables.
4. Update notebook table references.
5. Update dashboard datasets.
6. Validate lineage.
7. Update release docs.
