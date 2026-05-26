# Global Filter Propagation

## Purpose
This page documents the cross-dashboard filter architecture.

## Implemented Global Filters
- country
- geo_level
- state
- year
- quarter
- period

## Filter Propagation Model

Filters are intended to apply automatically to compatible widgets when dataset field names match.

Example:

```text
state filter
→ quarter_gold widgets
→ year_gold widgets
→ advanced analytics widgets where state exists
```

## Filter Compatibility

| Filter | Applies To |
|---|---|
| country | quarter_gold, year_gold, geo_readiness_summary |
| geo_level | quarter_gold, year_gold, geo_readiness_summary |
| state | quarter_gold, year_gold, top_10_states, rankings |
| year | quarter_gold, year_gold, growth datasets |
| quarter | quarter_gold, qoq/yoy datasets |
| period | quarter_gold, trend widgets |

## Governance Requirements
- All future datasets should include country when possible.
- All geo-enabled datasets should include geo_level.
- Period fields must be consistently formatted.
- Multi-country datasets must support country_code.

## Future Enhancements
- cascading filters
- county filters
- district filters
- zipcode filters
- map-linked filters
- global/regional hierarchy filters
