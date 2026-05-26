# ADR-004: Global Dashboard Filtering Framework

## Status
Accepted

## Context
The dashboard evolved into a multi-page enterprise analytics platform.

Initial filtering only supported:
- state
- year
- quarter

Future requirements introduced:
- multi-country analytics
- GIS drilldowns
- hierarchical geo navigation
- reusable dashboard governance

## Decision
Implement enterprise global filtering framework.

## Standard Filters
- country
- country_code
- geo_level
- state
- year
- quarter
- period

## Rationale
Global filters support:
- dashboard consistency
- executive slicing
- future geographic expansion
- reusable semantic datasets
- enterprise BI governance

## Consequences
### Positive
- consistent filtering experience
- multi-country readiness
- reusable widget architecture

### Risks
- filter propagation complexity
- widget synchronization overhead
- dashboard dependency management

## Future Enhancements
- cascading geo filters
- ZIP-level filtering
- GIS map synchronization
- district hierarchy navigation