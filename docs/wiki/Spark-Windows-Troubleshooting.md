# Spark Windows Troubleshooting
## USASpending Enterprise AI Medallion Solution

## Purpose
Documents Windows-specific Spark and PySpark issues encountered during local execution.

## Environment
- Windows 10/11
- Python 3.11
- Java 17 Temurin
- PySpark 3.5.1
- PowerShell

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
$env:PYTHONPATH=(Get-Location).Path
```

## Java Check
```powershell
java -version
```

## Common Fixes

### Missing packages
```powershell
python -m pip install requests pandas plotly flask pyarrow pyspark==3.5.1
```

### Hadoop warnings
`winutils.exe` and `NativeCodeLoader` warnings are usually non-blocking when the pipeline completes.

### Spark temp cleanup
`ShutdownHookManager` stack traces can happen after successful completion due to Windows file locking.

## Local Refresh
```powershell
python scripts\run_local.py --start-year 2024 --end-year 2025 --states PA NJ NY CA TX
```

## Suppress non-critical stderr
```powershell
python scripts\run_local.py --start-year 2024 --end-year 2025 --states PA NJ NY CA TX 2>spark_errors.log
```

## Production Direction
Use Databricks and Delta Lake for managed Spark execution.
