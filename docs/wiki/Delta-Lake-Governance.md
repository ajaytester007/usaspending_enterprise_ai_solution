# Delta Lake Governance

## Purpose
Defines Delta Lake governance practices for the solution.

## Current Delta Tables
- default.usaspending_state_quarter_silver
- default.usaspending_state_quarter_gold
- default.usaspending_state_year_gold
- default.usaspending_observability_refresh_log
- default.usaspending_observability_quality

## Governance Principles
- schema changes must be documented
- overwriteSchema must be controlled
- Gold tables should be treated as certified analytics
- Observability tables should be append-friendly
- Dashboard datasets should query Gold/Observability only

## Time Travel
Delta Lake time travel enables:

```sql
SELECT *
FROM table VERSION AS OF 15;
```

Use cases:
- rollback
- auditability
- historical replay
- compliance review
- release validation

## Future Enhancements
- table comments
- constraints
- generated columns
- change data feed
- quality expectations
- Unity Catalog migration
