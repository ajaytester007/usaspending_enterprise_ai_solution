# ADR-006: Multi-Country Expansion Architecture

## Status
Accepted

## Context
The platform evolved beyond US-only analytics.

Future goals include:
- international public spending analytics
- global dashboard filtering
- currency normalization
- GIS expansion
- connector abstraction

Target regions include:
- India
- UK
- Canada
- Brazil
- Japan
- Singapore
- France
- South Africa
- Nigeria

## Decision
Design platform around a canonical multi-country analytical schema.

## Canonical Schema
- country
- country_code
- geo_level
- geography_name
- currency_code
- period
- amount
- transaction_count
- source_system

## Connector Architecture

/connectors
    /usa
    /india
    /uk
    /canada

## Rationale
Canonical schema enables:
- dashboard reuse
- cross-country analytics
- consistent governance
- semantic analytical abstraction

## Consequences
### Positive
- scalable international architecture
- reusable analytical patterns
- future AI extensibility

### Risks
- varying country data quality
- currency conversion complexity
- fiscal calendar differences
- geography inconsistencies

## Future Enhancements
- FX normalization
- GIS hierarchy expansion
- AI-driven translation
- global observability
- geopolitical risk overlays