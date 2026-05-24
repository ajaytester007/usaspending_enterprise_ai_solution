# Medallion Architecture

## Bronze
Raw source-aligned data.
- USAspending API JSON payloads
- Request body and endpoint metadata
- Run timestamp and raw file lineage

## Silver
Validated and normalized analytical records.
- `source`
- `state`
- `year`
- `quarter`
- `period_start`
- `period_end`
- `total_obligations`
- `transaction_count`
- `raw_file`

## Gold
Business-ready reporting views.
- `state_quarter_summary`
- `state_year_summary`
- future: agency drill-down, recipient drill-down, award-type drill-down

## Quality Gates
- Schema validation
- Null checks
- Duplicate detection
- Freshness checks
- Traceability from gold to silver to bronze raw file
