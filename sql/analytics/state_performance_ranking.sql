WITH state_totals AS (
  SELECT
    state,
    SUM(total_obligations) AS total_obligations,
    SUM(transaction_count) AS transaction_count,
    TRY_DIVIDE(SUM(total_obligations), SUM(transaction_count)) AS avg_transaction_size
  FROM default.usaspending_state_quarter_gold
  GROUP BY state
),
total_spending AS (
  SELECT SUM(total_obligations) AS grand_total
  FROM state_totals
)
SELECT
  ROW_NUMBER() OVER (ORDER BY st.total_obligations DESC) AS rank,
  st.state,
  st.total_obligations,
  st.transaction_count,
  st.avg_transaction_size,
  (st.total_obligations / t.grand_total) * 100 AS pct_of_total,
  SUM(st.total_obligations) OVER (
    ORDER BY st.total_obligations DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) / t.grand_total * 100 AS cumulative_pct
FROM state_totals st
CROSS JOIN total_spending t
ORDER BY st.total_obligations DESC;
