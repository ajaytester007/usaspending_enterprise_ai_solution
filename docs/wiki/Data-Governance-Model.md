# Data Governance Model
## USASpending Enterprise AI Medallion Solution

## Purpose
Defines governance for quality, metadata, lineage, releases, and auditability.

## Data Layers
| Layer | Role |
|---|---|
| Bronze | Raw ingestion |
| Silver | Standardized model |
| Gold | Certified analytics |
| Observability | Operational controls |
| Dashboard | Consumption layer |

## Metadata Fields
```text
source_system
load_timestamp
refresh_id
environment
pipeline_name
country
geo_level
```

## Quality Dimensions
| Dimension | Example |
|---|---|
| Completeness | required fields not null |
| Validity | state codes valid |
| Consistency | period format valid |
| Accuracy | totals match source |
| Timeliness | latest period available |
| Uniqueness | no duplicate keys |

## Quality Rules
```text
state must not contain comma
year must be integer
period must match YYYY-Q#
total_obligations must be numeric
transaction_count must be numeric
country must not be null
```

## Lineage
```text
USAspending API -> Silver Delta -> Gold Delta -> Dashboard
```

## Release Governance
Every release should include source commit, tag, release notes, notebook export, dashboard SQL, and runbook updates.

## Future Governance
- Unity Catalog
- table owners
- schema permissions
- audit logging
- table comments
- certified datasets
