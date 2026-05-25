SELECT state, latest_year, latest_period, period_count, total_obligations, refresh_timestamp_utc
FROM default.usaspending_observability_freshness
ORDER BY state;
