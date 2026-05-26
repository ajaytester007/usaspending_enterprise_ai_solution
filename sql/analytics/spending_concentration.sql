WITH ranked_states AS (
  SELECT
    state,
    SUM(total_obligations) AS total_obligations,
    ROW_NUMBER() OVER (ORDER BY SUM(total_obligations) DESC) AS rank
  FROM default.usaspending_state_quarter_gold
  GROUP BY state
)
SELECT
  CASE WHEN rank <= 5 THEN state ELSE 'Others' END AS state_group,
  SUM(total_obligations) AS total_obligations
FROM ranked_states
GROUP BY state_group;
