SELECT refresh_timestamp_utc, metric_name, metric_value
FROM default.usaspending_observability_quality
ORDER BY refresh_timestamp_utc DESC, metric_name;
