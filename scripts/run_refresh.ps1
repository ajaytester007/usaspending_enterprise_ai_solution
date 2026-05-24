param(
  [int]$StartYear = 2024,
  [int]$EndYear = 2025,
  [string[]]$States = @('PA','NJ','NY','CA','TX')
)

.\.venv\Scripts\Activate.ps1
python scripts\run_local.py --start-year $StartYear --end-year $EndYear --states $States
python app\flask_app.py
