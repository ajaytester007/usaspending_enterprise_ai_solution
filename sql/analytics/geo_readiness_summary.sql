SELECT
  country,
  country_code,
  geo_level,
  COUNT(DISTINCT state) AS geography_count,
  COUNT(DISTINCT period) AS period_count,
  SUM(total_obligations) AS total_obligations,
  SUM(transaction_count) AS transaction_count
FROM default.usaspending_state_quarter_gold
GROUP BY
  country,
  country_code,
  geo_level;
