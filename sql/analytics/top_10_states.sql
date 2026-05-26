SELECT
  state,
  SUM(total_obligations) AS total_obligations,
  SUM(transaction_count) AS transaction_count
FROM default.usaspending_state_quarter_gold
GROUP BY state
ORDER BY total_obligations DESC
LIMIT 10;
