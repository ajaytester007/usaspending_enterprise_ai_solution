# Connectors

## Purpose
This folder contains source-specific ingestion adapters.

## Planned Connector Folders

```text
connectors/
  usa/
  india/
  uk/
  eu/
  canada/
```

## Connector Contract
Each connector must output:

```text
country
country_code
geo_level
geography_name
period
currency
amount
transaction_count
source_system
ingestion_timestamp
```
