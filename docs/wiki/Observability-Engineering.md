# Observability Engineering

## Purpose
This page defines the engineering approach for operational visibility.

## Observability Layers

### Pipeline Observability
Tracks execution status, row counts, and refresh metadata.

### Data Quality Observability
Tracks nulls, invalid values, stale data, and known metric defects.

### Dashboard Observability
Tracks dashboard readiness, refresh status, and widget degradation.

## Current Tables
- default.usaspending_observability_refresh_log
- default.usaspending_observability_quality
- default.usaspending_observability_freshness

## Recommended Additional Tables
- default.usaspending_observability_incidents
- default.usaspending_observability_alerts
- default.usaspending_observability_schema_changes
- default.usaspending_observability_api_calls

## Key Metrics
- refresh status
- refresh timestamp
- row count silver
- row count gold quarter
- row count gold year
- quality failure count
- stale period count
- known issue count

## Future Alerting
Trigger alerts when:
- refresh fails
- row count is zero
- null quality spikes
- QoQ growth exceeds threshold
- new schema drift appears
- source API failures exceed threshold
