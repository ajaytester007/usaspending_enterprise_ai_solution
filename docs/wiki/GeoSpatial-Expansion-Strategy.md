# GeoSpatial Expansion Strategy

## Purpose
Defines the path from state-level analytics to GIS-enabled public spend intelligence.

## Target Geography Columns
- country
- country_code
- geo_level
- state
- county
- district
- zipcode
- city
- latitude
- longitude
- fips_code

## Proposed GIS Tables
- us_geo_states
- us_geo_counties
- us_zipcodes
- us_congressional_districts

## Reference Sources
- Census TIGER
- GeoJSON boundary files
- FIPS mappings
- ZIP code reference files
- congressional district boundaries

## Planned Visualizations
- choropleth maps
- county heatmaps
- congressional district analytics
- ZIP-level spend analysis
- city-level drilldowns

## Implementation Phases
1. Add geo schema columns.
2. Add state GIS reference table.
3. Add county reference table.
4. Add ZIP reference table.
5. Add dashboard map widgets.
6. Add GIS observability and quality checks.
