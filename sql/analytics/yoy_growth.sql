SELECT
  curr.state,
  curr.quarter,
  curr.year AS current_year,
  curr.total_obligations AS current_obligations,
  prev.total_obligations AS previous_obligations,
  CASE
    WHEN prev.total_obligations > 0
    THEN ((curr.total_obligations - prev.total_obligations) / prev.total_obligations) * 100
    ELSE NULL
  END AS yoy_growth_pct
FROM default.usaspending_state_quarter_gold curr
LEFT JOIN default.usaspending_state_quarter_gold prev
  ON curr.state = prev.state
 AND curr.quarter = prev.quarter
 AND curr.year = prev.year + 1
WHERE prev.total_obligations IS NOT NULL;
