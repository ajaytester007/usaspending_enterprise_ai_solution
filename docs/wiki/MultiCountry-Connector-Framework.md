# MultiCountry Connector Framework

## Purpose
Defines the architecture for scaling the platform across countries.

## Connector Directory Model

```text
connectors/
  usa/
  india/
  uk/
  eu/
  canada/
```

## Connector Contract
Each connector must output a canonical schema:

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

## Planned Countries
- USA
- India
- UK
- Canada
- EU
- Brazil
- Mexico
- France
- Japan
- Singapore
- South Africa
- Nigeria

## Connector Responsibilities
- source API/file access
- source-specific parsing
- currency handling
- geography normalization
- metadata capture
- quality checks
- canonical output

## Future Enhancements
- connector registry
- source reliability scoring
- country-specific fiscal calendars
- multilingual metadata
- currency normalization
