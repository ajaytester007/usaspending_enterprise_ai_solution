# Scatter Analytics Model

## Purpose

Scatter analytics provide exploratory analytical capability for:
- volume vs value analysis
- outlier identification
- geographic comparison
- concentration detection
- anomaly exploration

---

# Current Scatter Dimensions

## Planned Primary Scatter

| X-axis | Y-axis |
|---|---|
| transaction_count | total_obligations |

## Secondary Scatter Options

| X-axis | Y-axis |
|---|---|
| avg_transaction_size | total_obligations |
| growth_percentage | obligations |
| state_rank | obligations |

---

# Current Known Limitation

KI-001 currently impacts:
- transaction-based scatter analytics
- average transaction size calculations

Current mitigation:
- use obligation-based scatter alternatives temporarily

---

# Future Enhancements

## Planned Features

- bubble size dimensions
- animated period transitions
- GIS overlays
- clustering analysis
- anomaly highlighting
- ML-based outlier detection

---

# Planned ML Integration

Future integrations:
- DBSCAN clustering
- KMeans grouping
- anomaly scoring
- outlier classification

---

# Recommended Executive Use Cases

- identify high-value low-volume states
- identify anomalous spend patterns
- identify concentration risk
- compare state efficiency
- monitor growth outliers
