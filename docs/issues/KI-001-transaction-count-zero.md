# KI-001: transaction_count Values Are Zero

## Status
Open

## Severity
Sev 3 - Analytics Degradation

## Discovered During
Advanced Analytics dashboard enhancement and scatter analytics implementation.

---

# Summary

The `transaction_count` metric currently resolves to zero across analytical outputs.

This affects all analytics and widgets dependent on transaction volume.

The issue was discovered during implementation of:
- scatter analytics
- ranking analytics
- average transaction size calculations
- advanced KPI visualizations

---

# Affected Components

## Affected Delta Tables

```text
default.usaspending_state_quarter_gold
default.usaspending_state_year_gold
```

Potential upstream source:

```text
default.usaspending_state_quarter_silver
```

---

# Affected Dashboard Widgets

| Widget | Impact |
|---|---|
| Transactions KPI | Incorrect or zero |
| Avg Transaction Size | Invalid / null |
| Scatter Plot | X-axis collapses |
| Ranking Analytics | Degraded scoring |
| Executive KPI Cards | Misleading transaction metrics |

---

# Affected Analytical Models

| Model | Impact |
|---|---|
| Scatter Analytics | Degraded |
| Ranking Models | Partial degradation |
| Transaction Density Analytics | Blocked |
| Average Size Metrics | Invalid |
| Volume vs Value Analysis | Degraded |

---

# Root Cause Hypothesis

The current ingestion logic likely does not extract the correct transaction count field from the USAspending API payload.

Current logic:

```python
count = sum(
    int(x.get("transaction_count", 0) or 0)
    for x in payload.get("results", [])
)
```

If `transaction_count` does not exist in the payload, the aggregation defaults to zero.

---

# Possible Root Causes

1. API field mismatch
2. Endpoint does not return transaction counts
3. Incorrect aggregation field
4. Payload structure differs from expectation
5. Counts require a separate endpoint

---

# Diagnostic Procedure

Run:

```python
payload.get("results", [])[:3]
```

Verify whether the API returns:
- transaction_count
- award_count
- count
- number_of_transactions
- another equivalent metric

---

# Recommended Remediation

## Step 1
Inspect raw API payload.

## Step 2
Identify correct count field.

## Step 3
Update ingestion logic.

## Step 4
Rebuild Silver and Gold tables.

## Step 5
Refresh dashboard datasets.

## Step 6
Republish dashboard.

---

# Temporary Mitigation

Until fixed:
- prioritize obligation-based analytics
- mark transaction-based widgets as degraded
- document issue in release notes
- avoid executive interpretation of transaction KPIs

---

# Quality Rule To Add

```python
zero_transaction_count = silver_df.filter(
    F.col("transaction_count") == 0
).count()
```

Recommended metric:

```text
silver_zero_transaction_count_rows
```

---

# Acceptance Criteria For Closure

The issue may be closed only when:

- transaction_count > 0 for expected rows
- scatter plots show meaningful distribution
- avg_transaction_size computes correctly
- ranking analytics recover
- quality metric passes
- dashboard republished
- release notes updated
