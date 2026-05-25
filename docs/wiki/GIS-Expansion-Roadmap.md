# GIS Expansion Roadmap
## USASpending Enterprise AI Medallion Solution

## Purpose
Defines evolution from state-level analytics to geography-aware analytics.

## Current Baseline
- Country: USA
- Geo level: state
- States: PA, NJ, NY, CA, TX, FL
- Years: 2024, 2025, 2026

## Target Hierarchy
```text
Country
  -> State / Province
      -> County / District
          -> City
              -> ZIP / Postal Code
                  -> Latitude / Longitude
```

## Proposed Schema
```text
country
country_code
geo_level
state
state_name
county
county_fips
district
zip_code
latitude
longitude
period
total_obligations
transaction_count
source_system
```

## Dashboard Enhancements
- country filter
- geo_level filter
- state filter
- county filter
- district filter
- zip_code filter
- choropleth map
- top counties
- ZIP-level drilldown

## Phases
1. Add country and geo_level.
2. Add county-level US prototype.
3. Add ZIP-level enrichment.
4. Add GIS boundaries.
5. Add map widgets.
6. Add global connector registry.
