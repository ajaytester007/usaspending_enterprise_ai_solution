# Data Model

## Dimensions

### DimState
- state_code
- state_name
- census_region
- census_division

### DimTimeQuarter
- year
- quarter
- period
- period_start
- period_end
- fiscal_year
- fiscal_quarter

### DimConnector
- connector_name
- domain
- endpoint
- auth_required
- owner
- refresh_frequency

### DimAwardType
- award_type_code
- award_type_group
- award_type_description

## Facts

### FactFederalSpendQuarter
- state_code
- year
- quarter
- source
- total_obligations
- transaction_count
- raw_file
- load_run_id

### FactRefreshRun
- run_id
- connector_name
- started_at
- ended_at
- status
- records_read
- records_written
- error_count

## Lineage
Bronze raw file → Silver normalized fact → Gold dashboard mart → Flask/Plotly report.
