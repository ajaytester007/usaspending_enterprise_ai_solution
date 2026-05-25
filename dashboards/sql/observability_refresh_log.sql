SELECT pipeline_name, refresh_timestamp_utc, source, states_requested, years_requested,
       row_count_silver, row_count_gold_quarter, row_count_gold_year, status
FROM default.usaspending_observability_refresh_log
ORDER BY refresh_timestamp_utc DESC;
