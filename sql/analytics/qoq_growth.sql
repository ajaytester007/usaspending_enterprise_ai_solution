WITH ordered_quarters AS (
  SELECT
    state,
    period,
    year,
    quarter,
    total_obligations,
    LAG(total_obligations) OVER (
      PARTITION BY state
      ORDER BY year, quarter
    ) AS prev_quarter_obligations
  FROM default.usaspending_state_quarter_gold
)
SELECT
  state,
  period,
  year,
  quarter,
  total_obligations AS current_obligations,
  prev_quarter_obligations,
  CASE
    WHEN prev_quarter_obligations > 0
    THEN ((total_obligations - prev_quarter_obligations) / prev_quarter_obligations) * 100
    ELSE NULL
  END AS qoq_growth_pct
FROM ordered_quarters
WHERE prev_quarter_obligations IS NOT NULL;
