@'
# Architecture

## Medallion Flow

USAspending API
-> Bronze Raw JSON
-> Silver Canonical Facts
-> Gold Aggregates
-> Flask Dashboard
-> Future Databricks Delta Lake

## Layer Responsibilities

### Bronze
Preserves raw USAspending API payloads.

### Silver
Standardized state-quarter datasets.

### Gold
Reporting and dashboard aggregates.
'@ | Set-Content docs\wiki\Architecture.md