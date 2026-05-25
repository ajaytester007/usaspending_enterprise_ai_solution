# Troubleshooting Runbook
## USASpending Enterprise AI Medallion Solution

## Purpose
Captures repeatable fixes and operational lessons discovered while stabilizing local PySpark, Databricks, GitHub, dashboard, and release workflows.

## Local PySpark Issues

### ModuleNotFoundError: No module named 'pyspark'
```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install pyspark==3.5.1
```

### ModuleNotFoundError: No module named 'src'
```powershell
$env:PYTHONPATH=(Get-Location).Path
python scripts\run_local.py --start-year 2024 --end-year 2025 --states PA NJ NY CA TX
```

### HADOOP_HOME / winutils warnings
Non-blocking if the pipeline ends with:

```text
Medallion pipeline complete.
Local refresh complete.
```

### Spark temp cleanup stack traces
Windows Spark can print `ShutdownHookManager` cleanup errors after successful execution. Treat as non-blocking when Silver/Gold outputs are created.

## Databricks Notebook Issues

### NameError: silver_df not defined
Run cells in order:
1. Config
2. Silver ingestion
3. Gold aggregation
4. Observability
5. SQL validation

### continue not properly in loop
Ensure `continue` remains inside the state loop:
```python
if not success:
    print(f"Skipping {state} {year} {quarter}")
    continue
```

### FL / 2026 not appearing
Remove hardcoded downstream config values. Keep these only in the config cell:
```python
states = ["PA", "NJ", "NY", "CA", "TX", "FL"]
years = [2024, 2025, 2026]
```

### TX and FL combined
Bad:
```python
states = ["PA", "NJ", "NY", "CA", "TX, FL"]
```
Good:
```python
states = ["PA", "NJ", "NY", "CA", "TX", "FL"]
```

Validation:
```sql
SELECT DISTINCT state
FROM default.usaspending_state_quarter_gold
ORDER BY state;
```

## Dashboard Issues

### Dashboard not reflecting new data
1. Run config cell.
2. Run ingestion.
3. Run Gold aggregation.
4. Run observability.
5. Validate Delta tables.
6. Refresh dashboard datasets.
7. Refresh dashboard canvas.
8. Clear stale filters.

## GitHub Issues

### fatal: not a git repository
```powershell
git init
```

### Permission denied on .vs
Add to `.gitignore`:
```gitignore
.vs/
.vscode/
.venv/
__pycache__/
```

### Release tag already exists
```powershell
gh release create v1.0.0 --verify-tag --title "USASpending Enterprise AI Solution v1.0.0" --notes "Initial enterprise release."
```
