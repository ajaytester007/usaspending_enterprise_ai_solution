"""
Databricks Integration Tests

These tests require:
- Databricks runtime
- Delta tables
- SQL Warehouse access

Not intended for local execution.
"""

# Databricks notebook source
# DBTITLE 1,Introduction
# MAGIC %md
# MAGIC # USASpending Federal Spend - SQL Queries and Tests
# MAGIC
# MAGIC This notebook contains comprehensive SQL queries and data quality tests for the **USASpending Federal Spend Medallion Dashboard**.
# MAGIC
# MAGIC ## Data Sources
# MAGIC - **default.usaspending_state_quarter_gold** - Quarterly federal spending by state
# MAGIC   - Columns: country, country_code, geo_level, state, year, quarter, period, total_obligations, transaction_count
# MAGIC - **default.usaspending_state_year_gold** - Yearly aggregations
# MAGIC
# MAGIC ## Notebook Structure
# MAGIC 1. **Core Data Queries** - Essential analytical queries for dashboard metrics
# MAGIC 2. **Data Quality Tests** - Validation tests to ensure data integrity
# MAGIC 3. **Advanced Analytics** - Statistical analysis and trend detection
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,Section 1: Core Data Queries
# MAGIC %md
# MAGIC ## Section 1: Core Data Queries
# MAGIC
# MAGIC These queries provide the fundamental metrics and analyses used across the dashboard.

# COMMAND ----------

# DBTITLE 1,Query 1: Total Spending by State
# MAGIC %md
# MAGIC ### Query 1: Total Spending by State
# MAGIC
# MAGIC Aggregates total obligations and transaction counts by state across all time periods. Useful for understanding which states receive the most federal spending.

# COMMAND ----------

# DBTITLE 1,Total Spending by State
# MAGIC %sql
# MAGIC -- Total federal spending by state
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   SUM(transaction_count) as total_transactions,
# MAGIC   ROUND(SUM(total_obligations) / NULLIF(SUM(transaction_count), 0), 2) as avg_transaction_size,
# MAGIC   COUNT(DISTINCT year) as years_with_data,
# MAGIC   COUNT(DISTINCT quarter) as quarters_with_data
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE state IS NOT NULL
# MAGIC GROUP BY state
# MAGIC ORDER BY total_obligations DESC

# COMMAND ----------

# DBTITLE 1,Query 2: Year-over-Year Growth
# MAGIC %md
# MAGIC ### Query 2: Year-over-Year Growth Analysis
# MAGIC
# MAGIC Calculates year-over-year growth rates for each state and quarter combination. Identifies which states are experiencing growth or decline in federal spending.

# COMMAND ----------

# DBTITLE 1,Year-over-Year Growth
# MAGIC %sql
# MAGIC -- Year-over-year growth analysis by state and quarter
# MAGIC WITH current_year AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     year,
# MAGIC     quarter,
# MAGIC     period,
# MAGIC     SUM(total_obligations) as current_obligations,
# MAGIC     SUM(transaction_count) as current_transactions
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state, year, quarter, period
# MAGIC ),
# MAGIC previous_year AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     year + 1 as year,  -- Join to next year
# MAGIC     quarter,
# MAGIC     SUM(total_obligations) as previous_obligations,
# MAGIC     SUM(transaction_count) as previous_transactions
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state, year, quarter
# MAGIC )
# MAGIC SELECT 
# MAGIC   cy.state,
# MAGIC   cy.year as current_year,
# MAGIC   cy.quarter,
# MAGIC   cy.period,
# MAGIC   cy.current_obligations,
# MAGIC   py.previous_obligations,
# MAGIC   ROUND(((cy.current_obligations - py.previous_obligations) / py.previous_obligations) * 100, 2) as yoy_growth_pct,
# MAGIC   cy.current_transactions,
# MAGIC   py.previous_transactions
# MAGIC FROM current_year cy
# MAGIC LEFT JOIN previous_year py ON cy.state = py.state AND cy.year = py.year AND cy.quarter = py.quarter
# MAGIC WHERE py.previous_obligations IS NOT NULL  -- Only show records with prior year data
# MAGIC ORDER BY cy.state, cy.year, cy.quarter

# COMMAND ----------

# DBTITLE 1,Query 3: Quarter-over-Quarter Growth
# MAGIC %md
# MAGIC ### Query 3: Quarter-over-Quarter Growth Analysis
# MAGIC
# MAGIC Tracks sequential quarter growth using LAG window function. Helps identify seasonal trends and short-term spending changes.

# COMMAND ----------

# DBTITLE 1,Quarter-over-Quarter Growth
# MAGIC %sql
# MAGIC -- Quarter-over-quarter growth analysis using LAG window function
# MAGIC WITH quarterly_data AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     year,
# MAGIC     quarter,
# MAGIC     period,
# MAGIC     SUM(total_obligations) as current_obligations,
# MAGIC     SUM(transaction_count) as current_transactions
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state, year, quarter, period
# MAGIC )
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   period,
# MAGIC   current_obligations,
# MAGIC   LAG(current_obligations, 1) OVER (PARTITION BY state ORDER BY year, quarter) as prev_quarter_obligations,
# MAGIC   ROUND(
# MAGIC     ((current_obligations - LAG(current_obligations, 1) OVER (PARTITION BY state ORDER BY year, quarter)) 
# MAGIC     / LAG(current_obligations, 1) OVER (PARTITION BY state ORDER BY year, quarter)) * 100, 
# MAGIC     2
# MAGIC   ) as qoq_growth_pct,
# MAGIC   current_transactions,
# MAGIC   LAG(current_transactions, 1) OVER (PARTITION BY state ORDER BY year, quarter) as prev_quarter_transactions
# MAGIC FROM quarterly_data
# MAGIC ORDER BY state, year, quarter

# COMMAND ----------

# DBTITLE 1,Query 4: Top 10 States
# MAGIC %md
# MAGIC ### Query 4: Top 10 States by Total Obligations
# MAGIC
# MAGIC Identifies the top 10 states with the highest total federal spending. This is a key metric for executive summaries.

# COMMAND ----------

# DBTITLE 1,Top 10 States
# MAGIC %sql
# MAGIC -- Top 10 states by total federal obligations
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   SUM(transaction_count) as total_transactions,
# MAGIC   ROUND(SUM(total_obligations) / NULLIF(SUM(transaction_count), 0), 2) as avg_transaction_size,
# MAGIC   COUNT(DISTINCT CONCAT(year, '-', quarter)) as total_quarters
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE state IS NOT NULL
# MAGIC GROUP BY state
# MAGIC ORDER BY total_obligations DESC
# MAGIC LIMIT 10

# COMMAND ----------

# DBTITLE 1,Query 5: State Performance Ranking
# MAGIC %md
# MAGIC ### Query 5: State Performance Ranking with Percentiles
# MAGIC
# MAGIC Ranks all states by total spending with cumulative percentages. Shows the concentration of spending and identifies which states account for specific thresholds (e.g., top 80% of spending).

# COMMAND ----------

# DBTITLE 1,State Performance Ranking
# MAGIC %sql
# MAGIC -- State performance ranking with cumulative percentages
# MAGIC WITH state_totals AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     SUM(total_obligations) as total_obligations,
# MAGIC     SUM(transaction_count) as total_transactions,
# MAGIC     ROUND(SUM(total_obligations) / SUM(transaction_count), 2) as avg_transaction_size
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state
# MAGIC ),
# MAGIC total_spending AS (
# MAGIC   SELECT SUM(total_obligations) as grand_total
# MAGIC   FROM state_totals
# MAGIC )
# MAGIC SELECT 
# MAGIC   ROW_NUMBER() OVER (ORDER BY st.total_obligations DESC) as rank,
# MAGIC   st.state,
# MAGIC   st.total_obligations,
# MAGIC   st.total_transactions,
# MAGIC   st.avg_transaction_size,
# MAGIC   ROUND((st.total_obligations / ts.grand_total) * 100, 2) as pct_of_total,
# MAGIC   ROUND(SUM(st.total_obligations) OVER (ORDER BY st.total_obligations DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / ts.grand_total * 100, 2) as cumulative_pct
# MAGIC FROM state_totals st
# MAGIC CROSS JOIN total_spending ts
# MAGIC ORDER BY st.total_obligations DESC

# COMMAND ----------

# DBTITLE 1,Query 6: Spending Concentration
# MAGIC %md
# MAGIC ### Query 6: Spending Concentration (Top 5 vs Others)
# MAGIC
# MAGIC Analyzes spending concentration by comparing top 5 states against all others. Useful for pie charts and understanding spending distribution.

# COMMAND ----------

# DBTITLE 1,Spending Concentration
# MAGIC %sql
# MAGIC -- Spending concentration: Top 5 states vs Others
# MAGIC WITH ranked_states AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     SUM(total_obligations) as total_obligations,
# MAGIC     ROW_NUMBER() OVER (ORDER BY SUM(total_obligations) DESC) as rank
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state
# MAGIC )
# MAGIC SELECT 
# MAGIC   CASE 
# MAGIC     WHEN rank <= 5 THEN state 
# MAGIC     ELSE 'Others' 
# MAGIC   END as state_group,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   COUNT(DISTINCT CASE WHEN rank > 5 THEN state END) as num_states_in_others
# MAGIC FROM ranked_states
# MAGIC GROUP BY state_group
# MAGIC ORDER BY total_obligations DESC

# COMMAND ----------

# DBTITLE 1,Query 7: Average Transaction Size
# MAGIC %md
# MAGIC ### Query 7: Average Transaction Size by State and Year
# MAGIC
# MAGIC Calculates average transaction size (total obligations / transaction count) over time. Helps identify states with larger or smaller individual transactions.

# COMMAND ----------

# DBTITLE 1,Average Transaction Size
# MAGIC %sql
# MAGIC -- Average transaction size by state and year
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   SUM(transaction_count) as total_transactions,
# MAGIC   ROUND(SUM(total_obligations) / NULLIF(SUM(transaction_count), 0), 2) as avg_transaction_size,
# MAGIC   ROUND(MIN(total_obligations / NULLIF(transaction_count, 0)), 2) as min_transaction_size,
# MAGIC   ROUND(MAX(total_obligations / NULLIF(transaction_count, 0)), 2) as max_transaction_size
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE state IS NOT NULL 
# MAGIC   AND transaction_count > 0
# MAGIC GROUP BY state, year
# MAGIC ORDER BY state, year

# COMMAND ----------

# DBTITLE 1,Section 2: Data Quality Tests
# MAGIC %md
# MAGIC ---
# MAGIC ## Section 2: Data Quality Tests
# MAGIC
# MAGIC These tests validate data integrity, completeness, and consistency. Each test returns a PASS/FAIL status with details.

# COMMAND ----------

# DBTITLE 1,Test 1: Row Count Validation
# MAGIC %md
# MAGIC ### Test 1: Row Count Validation
# MAGIC
# MAGIC Verifies that both tables contain data and checks for reasonable row counts.

# COMMAND ----------

# DBTITLE 1,Test 1: Row Count
# MAGIC %sql
# MAGIC -- Test 1: Row count validation
# MAGIC WITH quarterly_count AS (
# MAGIC   SELECT 'quarterly_table' as table_name, COUNT(*) as row_count
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC ),
# MAGIC yearly_count AS (
# MAGIC   SELECT 'yearly_table' as table_name, COUNT(*) as row_count
# MAGIC   FROM default.usaspending_state_year_gold
# MAGIC ),
# MAGIC combined AS (
# MAGIC   SELECT * FROM quarterly_count
# MAGIC   UNION ALL
# MAGIC   SELECT * FROM yearly_count
# MAGIC )
# MAGIC SELECT 
# MAGIC   table_name,
# MAGIC   row_count,
# MAGIC   CASE 
# MAGIC     WHEN row_count > 0 THEN 'PASS'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CASE 
# MAGIC     WHEN row_count = 0 THEN 'ERROR: Table is empty'
# MAGIC     ELSE 'Table contains data'
# MAGIC   END as message
# MAGIC FROM combined

# COMMAND ----------

# DBTITLE 1,Test 2: NULL Value Checks
# MAGIC %md
# MAGIC ### Test 2: NULL Value Checks for Critical Columns
# MAGIC
# MAGIC Ensures that critical columns (state, year, quarter, total_obligations, transaction_count) do not contain NULL values.

# COMMAND ----------

# DBTITLE 1,Test 2: NULL Checks
# MAGIC %sql
# MAGIC -- Test 2: NULL value checks for critical columns
# MAGIC SELECT 
# MAGIC   'state' as column_name,
# MAGIC   COUNT(*) as null_count,
# MAGIC   ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM default.usaspending_state_quarter_gold)), 2) as null_pct,
# MAGIC   CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as test_status
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE state IS NULL
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 
# MAGIC   'year' as column_name,
# MAGIC   COUNT(*) as null_count,
# MAGIC   ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM default.usaspending_state_quarter_gold)), 2) as null_pct,
# MAGIC   CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as test_status
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE year IS NULL
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 
# MAGIC   'quarter' as column_name,
# MAGIC   COUNT(*) as null_count,
# MAGIC   ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM default.usaspending_state_quarter_gold)), 2) as null_pct,
# MAGIC   CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as test_status
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE quarter IS NULL
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 
# MAGIC   'total_obligations' as column_name,
# MAGIC   COUNT(*) as null_count,
# MAGIC   ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM default.usaspending_state_quarter_gold)), 2) as null_pct,
# MAGIC   CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as test_status
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE total_obligations IS NULL
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 
# MAGIC   'transaction_count' as column_name,
# MAGIC   COUNT(*) as null_count,
# MAGIC   ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM default.usaspending_state_quarter_gold)), 2) as null_pct,
# MAGIC   CASE WHEN COUNT(*) = 0 THEN 'PASS' ELSE 'FAIL' END as test_status
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE transaction_count IS NULL

# COMMAND ----------

# DBTITLE 1,Test 3: Data Type Validation
# MAGIC %md
# MAGIC ### Test 3: Data Type and Value Range Validation
# MAGIC
# MAGIC Checks that numeric columns contain valid values and are within expected ranges.

# COMMAND ----------

# DBTITLE 1,Test 3: Data Types
# MAGIC %sql
# MAGIC -- Test 3: Data type and value range validation
# MAGIC SELECT 
# MAGIC   'year_range' as test_name,
# MAGIC   MIN(year) as min_value,
# MAGIC   MAX(year) as max_value,
# MAGIC   CASE 
# MAGIC     WHEN MIN(year) >= 2000 AND MAX(year) <= YEAR(CURRENT_DATE()) THEN 'PASS'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CONCAT('Year range: ', MIN(year), ' to ', MAX(year)) as message
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 
# MAGIC   'quarter_values' as test_name,
# MAGIC   COUNT(DISTINCT quarter) as min_value,
# MAGIC   NULL as max_value,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(DISTINCT quarter) <= 4 THEN 'PASS'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CONCAT('Found ', COUNT(DISTINCT quarter), ' distinct quarter values') as message
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 
# MAGIC   'obligations_positive' as test_name,
# MAGIC   COUNT(*) as min_value,
# MAGIC   NULL as max_value,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'PASS'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CONCAT(COUNT(*), ' records with negative obligations') as message
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE total_obligations < 0
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 
# MAGIC   'transaction_count_positive' as test_name,
# MAGIC   COUNT(*) as min_value,
# MAGIC   NULL as max_value,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'PASS'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CONCAT(COUNT(*), ' records with negative transaction counts') as message
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE transaction_count < 0

# COMMAND ----------

# DBTITLE 1,Test 4: Referential Integrity
# MAGIC %md
# MAGIC ### Test 4: Referential Integrity - State Codes
# MAGIC
# MAGIC Validates that state values are consistent and follow expected patterns (2-letter codes or full names).

# COMMAND ----------

# DBTITLE 1,Test 4: State Codes
# MAGIC %sql
# MAGIC -- Test 4: Referential integrity - State codes validation
# MAGIC WITH state_analysis AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     LENGTH(state) as state_length,
# MAGIC     COUNT(*) as record_count
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state, LENGTH(state)
# MAGIC ),
# MAGIC invalid_states AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     state_length,
# MAGIC     record_count
# MAGIC   FROM state_analysis
# MAGIC   WHERE state_length NOT IN (2) -- Expecting 2-letter state codes
# MAGIC     OR state NOT REGEXP '^[A-Z]{2}$' -- Must be 2 uppercase letters
# MAGIC )
# MAGIC SELECT 
# MAGIC   'state_code_format' as test_name,
# MAGIC   COALESCE(SUM(record_count), 0) as invalid_record_count,
# MAGIC   CASE 
# MAGIC     WHEN COALESCE(SUM(record_count), 0) = 0 THEN 'PASS'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CASE 
# MAGIC     WHEN COALESCE(SUM(record_count), 0) = 0 THEN 'All state codes are valid'
# MAGIC     ELSE CONCAT(CAST(SUM(record_count) AS STRING), ' records with invalid state codes: ', CONCAT_WS(', ', COLLECT_LIST(DISTINCT state)))
# MAGIC   END as message
# MAGIC FROM invalid_states

# COMMAND ----------

# DBTITLE 1,Test 5: Duplicate Detection
# MAGIC %md
# MAGIC ### Test 5: Duplicate Detection
# MAGIC
# MAGIC Checks for duplicate records based on unique key combinations (state, year, quarter).

# COMMAND ----------

# DBTITLE 1,Test 5: Duplicates
# MAGIC %sql
# MAGIC -- Test 5: Duplicate detection
# MAGIC WITH duplicate_check AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     year,
# MAGIC     quarter,
# MAGIC     COUNT(*) as occurrence_count
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state, year, quarter
# MAGIC   HAVING COUNT(*) > 1
# MAGIC )
# MAGIC SELECT 
# MAGIC   'duplicate_records' as test_name,
# MAGIC   COUNT(*) as duplicate_group_count,
# MAGIC   COALESCE(SUM(occurrence_count), 0) as total_duplicate_records,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'PASS'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'No duplicates found'
# MAGIC     ELSE CONCAT(COUNT(*), ' duplicate groups found affecting ', SUM(occurrence_count), ' total records')
# MAGIC   END as message
# MAGIC FROM duplicate_check

# COMMAND ----------

# DBTITLE 1,Test 6: Outlier Detection
# MAGIC %md
# MAGIC ### Test 6: Outlier Detection
# MAGIC
# MAGIC Identifies records with unusually high or low values using statistical thresholds (3 standard deviations).

# COMMAND ----------

# DBTITLE 1,Test 6: Outliers
# MAGIC %sql
# MAGIC -- Test 6: Outlier detection using 3 standard deviations
# MAGIC WITH stats AS (
# MAGIC   SELECT 
# MAGIC     AVG(total_obligations) as avg_obligations,
# MAGIC     STDDEV(total_obligations) as stddev_obligations
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE total_obligations IS NOT NULL
# MAGIC ),
# MAGIC outliers AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     year,
# MAGIC     quarter,
# MAGIC     total_obligations,
# MAGIC     (total_obligations - s.avg_obligations) / s.stddev_obligations as z_score
# MAGIC   FROM default.usaspending_state_quarter_gold q
# MAGIC   CROSS JOIN stats s
# MAGIC   WHERE ABS((total_obligations - s.avg_obligations) / s.stddev_obligations) > 3
# MAGIC )
# MAGIC SELECT 
# MAGIC   'outlier_detection' as test_name,
# MAGIC   COUNT(*) as outlier_count,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'PASS'
# MAGIC     WHEN COUNT(*) <= 10 THEN 'WARNING'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'No outliers detected'
# MAGIC     ELSE CONCAT(COUNT(*), ' outliers detected (>3 std dev from mean)')
# MAGIC   END as message
# MAGIC FROM outliers

# COMMAND ----------

# DBTITLE 1,Test 7: Temporal Consistency
# MAGIC %md
# MAGIC ### Test 7: Temporal Consistency - Quarter Gaps
# MAGIC
# MAGIC Detects missing quarters in the time series for each state. A complete dataset should have all 4 quarters for each year.

# COMMAND ----------

# DBTITLE 1,Test 7: Temporal Gaps
# MAGIC %sql
# MAGIC -- Test 7: Temporal consistency - Detect quarter gaps
# MAGIC WITH state_year_quarters AS (
# MAGIC   SELECT DISTINCT
# MAGIC     state,
# MAGIC     year,
# MAGIC     quarter
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC ),
# MAGIC quarter_list AS (
# MAGIC   SELECT 1 as quarter_num
# MAGIC   UNION ALL SELECT 2
# MAGIC   UNION ALL SELECT 3
# MAGIC   UNION ALL SELECT 4
# MAGIC ),
# MAGIC expected_quarters AS (
# MAGIC   SELECT DISTINCT
# MAGIC     syq.state,
# MAGIC     syq.year,
# MAGIC     ql.quarter_num as quarter
# MAGIC   FROM state_year_quarters syq
# MAGIC   CROSS JOIN quarter_list ql
# MAGIC ),
# MAGIC missing_quarters AS (
# MAGIC   SELECT 
# MAGIC     eq.state,
# MAGIC     eq.year,
# MAGIC     eq.quarter
# MAGIC   FROM expected_quarters eq
# MAGIC   LEFT JOIN state_year_quarters syq 
# MAGIC     ON eq.state = syq.state 
# MAGIC     AND eq.year = syq.year 
# MAGIC     AND CAST(eq.quarter AS STRING) = syq.quarter
# MAGIC   WHERE syq.quarter IS NULL
# MAGIC )
# MAGIC SELECT 
# MAGIC   'temporal_consistency' as test_name,
# MAGIC   COUNT(*) as missing_quarter_count,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'PASS'
# MAGIC     WHEN COUNT(*) <= 20 THEN 'WARNING'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'No missing quarters detected'
# MAGIC     ELSE CONCAT(CAST(COUNT(*) AS STRING), ' missing quarters detected across states')
# MAGIC   END as message
# MAGIC FROM missing_quarters

# COMMAND ----------

# DBTITLE 1,Test 8: Aggregation Reconciliation
# MAGIC %md
# MAGIC ### Test 8: Aggregation Reconciliation
# MAGIC
# MAGIC Verifies that quarterly sums match yearly aggregations in the yearly table. This ensures data consistency between the two tables.

# COMMAND ----------

# DBTITLE 1,Test 8: Reconciliation
# MAGIC %sql
# MAGIC -- Test 8: Aggregation reconciliation - Quarterly sums vs Yearly table
# MAGIC WITH quarterly_sums AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     year,
# MAGIC     SUM(total_obligations) as quarterly_total,
# MAGIC     SUM(transaction_count) as quarterly_transactions
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state, year
# MAGIC ),
# MAGIC yearly_data AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     year,
# MAGIC     total_obligations as yearly_total,
# MAGIC     transaction_count as yearly_transactions
# MAGIC   FROM default.usaspending_state_year_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC ),
# MAGIC comparison AS (
# MAGIC   SELECT 
# MAGIC     qs.state,
# MAGIC     qs.year,
# MAGIC     qs.quarterly_total,
# MAGIC     yd.yearly_total,
# MAGIC     ABS(qs.quarterly_total - yd.yearly_total) as difference,
# MAGIC     ROUND(ABS(qs.quarterly_total - yd.yearly_total) / NULLIF(yd.yearly_total, 0) * 100, 2) as pct_difference
# MAGIC   FROM quarterly_sums qs
# MAGIC   INNER JOIN yearly_data yd ON qs.state = yd.state AND qs.year = yd.year
# MAGIC   WHERE ABS(qs.quarterly_total - yd.yearly_total) / NULLIF(yd.yearly_total, 0) > 0.01 -- Allow 1% variance
# MAGIC )
# MAGIC SELECT 
# MAGIC   'aggregation_reconciliation' as test_name,
# MAGIC   COUNT(*) as mismatch_count,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'PASS'
# MAGIC     WHEN COUNT(*) <= 5 THEN 'WARNING'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'Quarterly and yearly aggregations match'
# MAGIC     ELSE CONCAT(COUNT(*), ' state-year combinations have mismatches >1%')
# MAGIC   END as message
# MAGIC FROM comparison

# COMMAND ----------

# DBTITLE 1,Test 9: Positive Obligations
# MAGIC %md
# MAGIC ### Test 9: Total Obligations Greater Than Zero
# MAGIC
# MAGIC Ensures that all records have positive total obligations. Federal spending should always be positive.

# COMMAND ----------

# DBTITLE 1,Test 9: Positive Values
# MAGIC %sql
# MAGIC -- Test 9: Total obligations > 0 validation
# MAGIC SELECT 
# MAGIC   'positive_obligations' as test_name,
# MAGIC   COUNT(*) as zero_or_negative_count,
# MAGIC   ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM default.usaspending_state_quarter_gold)), 2) as pct_of_total,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'PASS'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'All records have positive obligations'
# MAGIC     ELSE CONCAT(COUNT(*), ' records with zero or negative obligations')
# MAGIC   END as message
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE total_obligations <= 0

# COMMAND ----------

# DBTITLE 1,Test 10: Transaction Consistency
# MAGIC %md
# MAGIC ### Test 10: Transaction Count Consistency
# MAGIC
# MAGIC Validates that transaction counts are reasonable - records with obligations should have at least 1 transaction.

# COMMAND ----------

# DBTITLE 1,Test 10: Transaction Counts
# MAGIC %sql
# MAGIC -- Test 10: Transaction count consistency
# MAGIC SELECT 
# MAGIC   'transaction_consistency' as test_name,
# MAGIC   COUNT(*) as invalid_transaction_count,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'PASS'
# MAGIC     ELSE 'FAIL'
# MAGIC   END as test_status,
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) = 0 THEN 'All records with obligations have valid transaction counts'
# MAGIC     ELSE CONCAT(COUNT(*), ' records have obligations but zero/null transactions')
# MAGIC   END as message
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE total_obligations > 0 AND (transaction_count IS NULL OR transaction_count <= 0)

# COMMAND ----------

# DBTITLE 1,Test Results Summary
# MAGIC %md
# MAGIC ## 📊 Data Quality Test Results Summary
# MAGIC
# MAGIC ### ✅ PASSED Tests (7/10)
# MAGIC 1. **Test 1: Row Count Validation** - Both tables contain data (72 quarterly, 18 yearly)
# MAGIC 2. **Test 2: NULL Value Checks** - No NULL values in critical columns
# MAGIC 3. **Test 3: Data Type Validation** - All data types and ranges are valid
# MAGIC 4. **Test 4: State Code Format** - All state codes are valid 2-letter codes
# MAGIC 5. **Test 5: Duplicate Detection** - No duplicate records found
# MAGIC 6. **Test 6: Outlier Detection** - No statistical outliers detected
# MAGIC 8. **Test 8: Aggregation Reconciliation** - Quarterly sums match yearly aggregations
# MAGIC
# MAGIC ### ❌ FAILED Tests (3/10)
# MAGIC 7. **Test 7: Temporal Consistency** - **FAIL** - 72 missing quarters detected across states
# MAGIC    - Dataset may not have complete quarterly coverage for all state-year combinations
# MAGIC 9. **Test 9: Positive Obligations** - **FAIL** - 12 records (16.67%) have zero or negative obligations
# MAGIC    - Federal spending should always be positive
# MAGIC 10. **Test 10: Transaction Consistency** - **FAIL** - 60 records (83.33%) have obligations but zero transaction counts
# MAGIC    - Suggests transaction_count column needs to be populated
# MAGIC
# MAGIC ### 🔍 Key Data Quality Issues
# MAGIC 1. **Missing Transaction Counts**: 60 out of 72 records have zero transaction counts despite having obligations
# MAGIC 2. **Zero/Negative Obligations**: 12 records need investigation
# MAGIC 3. **Incomplete Time Series**: Missing quarterly data for some state-year combinations
# MAGIC
# MAGIC ### 📝 Recommendations
# MAGIC 1. Populate or recalculate the `transaction_count` column
# MAGIC 2. Investigate and correct records with zero/negative obligations
# MAGIC 3. Review data ingestion process to ensure complete quarterly coverage

# COMMAND ----------

# DBTITLE 1,Section 3: Advanced Analytics
# MAGIC %md
# MAGIC ---
# MAGIC ## Section 3: Advanced Analytics Queries
# MAGIC
# MAGIC These queries provide statistical analysis, trend detection, and advanced insights using window functions and aggregations.

# COMMAND ----------

# DBTITLE 1,Investigation: Zero Transaction Counts
# MAGIC %md
# MAGIC ---
# MAGIC ## 🔍 Investigation: Zero Transaction Counts Issue
# MAGIC
# MAGIC Based on Test 10, we found that **60 out of 72 records (83%)** have total obligations but zero transaction counts. This is a critical data quality issue that needs investigation.
# MAGIC
# MAGIC ### Questions to Answer:
# MAGIC 1. Which states are affected?
# MAGIC 2. Which time periods have zero transaction counts?
# MAGIC 3. Are there any patterns (specific years, quarters)?
# MAGIC 4. What's the distribution of records with vs without transaction counts?

# COMMAND ----------

# DBTITLE 1,Query 1: Overview of Transaction Count Issue
# MAGIC %md
# MAGIC ### Investigation Query 1: Overview of the Issue
# MAGIC
# MAGIC Get a high-level view of records with zero vs non-zero transaction counts.

# COMMAND ----------

# DBTITLE 1,Transaction Count Overview
# MAGIC %sql
# MAGIC -- Overview: Records with zero vs non-zero transaction counts
# MAGIC SELECT 
# MAGIC   CASE 
# MAGIC     WHEN transaction_count = 0 THEN 'Zero Transaction Count'
# MAGIC     WHEN transaction_count > 0 THEN 'Has Transaction Count'
# MAGIC     ELSE 'NULL Transaction Count'
# MAGIC   END as transaction_status,
# MAGIC   COUNT(*) as record_count,
# MAGIC   ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM default.usaspending_state_quarter_gold)), 2) as pct_of_total,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   ROUND(SUM(total_obligations) / 1e9, 2) as total_obligations_billions,
# MAGIC   COUNT(DISTINCT state) as distinct_states,
# MAGIC   COUNT(DISTINCT year) as distinct_years,
# MAGIC   COUNT(DISTINCT quarter) as distinct_quarters
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC GROUP BY transaction_status
# MAGIC ORDER BY record_count DESC

# COMMAND ----------

# DBTITLE 1,Query 2: States Affected
# MAGIC %md
# MAGIC ### Investigation Query 2: Which States Are Affected?
# MAGIC
# MAGIC Breakdown by state showing which states have zero transaction counts.

# COMMAND ----------

# DBTITLE 1,States with Zero Transactions
# MAGIC %sql
# MAGIC -- States affected by zero transaction counts
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   COUNT(*) as total_records,
# MAGIC   SUM(CASE WHEN transaction_count = 0 THEN 1 ELSE 0 END) as zero_transaction_records,
# MAGIC   SUM(CASE WHEN transaction_count > 0 THEN 1 ELSE 0 END) as has_transaction_records,
# MAGIC   ROUND((SUM(CASE WHEN transaction_count = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) as pct_zero_transactions,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   ROUND(SUM(total_obligations) / 1e9, 2) as total_obligations_billions,
# MAGIC   SUM(CASE WHEN transaction_count = 0 THEN total_obligations ELSE 0 END) as obligations_with_zero_transactions,
# MAGIC   ROUND(SUM(CASE WHEN transaction_count = 0 THEN total_obligations ELSE 0 END) / 1e9, 2) as obligations_zero_tx_billions
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC GROUP BY state
# MAGIC ORDER BY zero_transaction_records DESC, total_obligations DESC

# COMMAND ----------

# DBTITLE 1,Query 3: Time Period Analysis
# MAGIC %md
# MAGIC ### Investigation Query 3: Time Period Patterns
# MAGIC
# MAGIC Analyze which years and quarters are affected by zero transaction counts.

# COMMAND ----------

# DBTITLE 1,Time Period Analysis
# MAGIC %sql
# MAGIC -- Time period analysis: Which years/quarters have zero transaction counts?
# MAGIC SELECT 
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   period,
# MAGIC   COUNT(*) as total_records,
# MAGIC   SUM(CASE WHEN transaction_count = 0 THEN 1 ELSE 0 END) as zero_transaction_records,
# MAGIC   SUM(CASE WHEN transaction_count > 0 THEN 1 ELSE 0 END) as has_transaction_records,
# MAGIC   ROUND((SUM(CASE WHEN transaction_count = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) as pct_zero_transactions,
# MAGIC   COUNT(DISTINCT state) as states_affected,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   ROUND(SUM(total_obligations) / 1e9, 2) as total_obligations_billions
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC GROUP BY year, quarter, period
# MAGIC ORDER BY year, quarter

# COMMAND ----------

# DBTITLE 1,Query 4: Sample Records
# MAGIC %md
# MAGIC ### Investigation Query 4: Sample Records with Zero Transaction Counts
# MAGIC
# MAGIC Look at actual records to understand the data pattern.

# COMMAND ----------

# DBTITLE 1,Sample Zero Transaction Records
# MAGIC %sql
# MAGIC -- Sample of records with zero transaction counts
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   period,
# MAGIC   country,
# MAGIC   country_code,
# MAGIC   geo_level,
# MAGIC   total_obligations,
# MAGIC   ROUND(total_obligations / 1e9, 2) as obligations_billions,
# MAGIC   transaction_count
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE transaction_count = 0
# MAGIC ORDER BY total_obligations DESC
# MAGIC LIMIT 20

# COMMAND ----------

# DBTITLE 1,Query 5: Records WITH Transactions
# MAGIC %md
# MAGIC ### Investigation Query 5: Sample Records WITH Transaction Counts
# MAGIC
# MAGIC Compare against the records that DO have transaction counts to identify differences.

# COMMAND ----------

# DBTITLE 1,Sample Non-Zero Transaction Records
# MAGIC %sql
# MAGIC -- Sample of records WITH transaction counts (for comparison)
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   period,
# MAGIC   country,
# MAGIC   country_code,
# MAGIC   geo_level,
# MAGIC   total_obligations,
# MAGIC   ROUND(total_obligations / 1e9, 2) as obligations_billions,
# MAGIC   transaction_count,
# MAGIC   ROUND(total_obligations / NULLIF(transaction_count, 0), 2) as avg_transaction_size
# MAGIC FROM default.usaspending_state_quarter_gold
# MAGIC WHERE transaction_count > 0
# MAGIC ORDER BY total_obligations DESC
# MAGIC LIMIT 20

# COMMAND ----------

# DBTITLE 1,Query 6: Check Source Table
# MAGIC %md
# MAGIC ### Investigation Query 6: Check Yearly Table for Transaction Counts
# MAGIC
# MAGIC Check if the yearly aggregation table has the same issue.

# COMMAND ----------

# DBTITLE 1,Yearly Table Transaction Counts
# MAGIC %sql
# MAGIC -- Check yearly table for transaction count issue
# MAGIC SELECT 
# MAGIC   CASE 
# MAGIC     WHEN transaction_count = 0 THEN 'Zero Transaction Count'
# MAGIC     WHEN transaction_count > 0 THEN 'Has Transaction Count'
# MAGIC     ELSE 'NULL Transaction Count'
# MAGIC   END as transaction_status,
# MAGIC   COUNT(*) as record_count,
# MAGIC   ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM default.usaspending_state_year_gold)), 2) as pct_of_total,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   ROUND(SUM(total_obligations) / 1e9, 2) as total_obligations_billions,
# MAGIC   COUNT(DISTINCT state) as distinct_states
# MAGIC FROM default.usaspending_state_year_gold
# MAGIC GROUP BY transaction_status
# MAGIC ORDER BY record_count DESC

# COMMAND ----------

# DBTITLE 1,Investigation Findings & Recommendations
# MAGIC %md
# MAGIC ---
# MAGIC ## 🎯 Investigation Findings: Zero Transaction Counts
# MAGIC
# MAGIC ### Critical Discovery: 100% of Records Affected
# MAGIC
# MAGIC The investigation reveals that **ALL 72 quarterly records (100%)** and **ALL 18 yearly records (100%)** have zero transaction counts, despite having $1.64 trillion in total obligations.
# MAGIC
# MAGIC ### Detailed Findings
# MAGIC
# MAGIC #### 1. **Scope of Impact**
# MAGIC * **Quarterly Table**: 72 out of 72 records (100%) have `transaction_count = 0`
# MAGIC * **Yearly Table**: 18 out of 18 records (100%) have `transaction_count = 0`
# MAGIC * **Total Obligations**: $1,641.57 billion across all affected records
# MAGIC * **States Affected**: ALL 6 states (CA, TX, NY, FL, PA, NJ) - 100% affected
# MAGIC * **Time Periods**: ALL quarters from 2024-Q1 through 2026-Q2 - 100% affected
# MAGIC
# MAGIC #### 2. **State Breakdown**
# MAGIC | State | Records | Zero TX Count | Obligations (Billions) |
# MAGIC |-------|---------|---------------|------------------------|
# MAGIC | CA    | 12      | 12 (100%)     | $543.78               |
# MAGIC | TX    | 12      | 12 (100%)     | $344.23               |
# MAGIC | NY    | 12      | 12 (100%)     | $301.34               |
# MAGIC | FL    | 12      | 12 (100%)     | $182.71               |
# MAGIC | PA    | 12      | 12 (100%)     | $181.04               |
# MAGIC | NJ    | 12      | 12 (100%)     | $88.47                |
# MAGIC
# MAGIC #### 3. **Time Period Patterns**
# MAGIC * Every quarter from 2024-Q1 through 2026-Q2 has 6 records (one per state)
# MAGIC * ALL records in every quarter have zero transaction counts
# MAGIC * 2026-Q3 and 2026-Q4 have zero obligations (future quarters with no data)
# MAGIC * No temporal pattern - this is a **systematic issue across all time periods**
# MAGIC
# MAGIC #### 4. **Sample Data Example**
# MAGIC ```
# MAGIC State: CA, Period: 2025-Q3
# MAGIC Total Obligations: $68.44 billion
# MAGIC Transaction Count: 0  ⚠️
# MAGIC ```
# MAGIC
# MAGIC ### Root Cause Analysis
# MAGIC
# MAGIC **Conclusion**: This is NOT a data quality issue with missing or corrupted transactions. This is a **data ingestion/ETL issue** where the `transaction_count` column was **never populated** during the data loading process.
# MAGIC
# MAGIC **Evidence**:
# MAGIC 1. 100% of records are affected - no exceptions
# MAGIC 2. All states, all time periods uniformly affected
# MAGIC 3. NO records exist with non-zero transaction counts to compare against
# MAGIC 4. Both quarterly and yearly tables have the same issue
# MAGIC 5. Total obligations are present and appear reasonable
# MAGIC
# MAGIC ### Impact Assessment
# MAGIC
# MAGIC #### ❌ **Broken Functionality**
# MAGIC The following analyses CANNOT be performed:
# MAGIC * Average transaction size calculations
# MAGIC * Transaction count trends
# MAGIC * Transaction volume comparisons
# MAGIC * Per-transaction metrics
# MAGIC * Any query involving `transaction_count` column
# MAGIC
# MAGIC #### ✅ **Working Functionality**
# MAGIC The following analyses STILL WORK:
# MAGIC * Total obligations by state/time
# MAGIC * Year-over-year growth (based on obligations)
# MAGIC * Quarter-over-quarter growth (based on obligations)
# MAGIC * State rankings by spending
# MAGIC * Spending concentration analysis
# MAGIC
# MAGIC ### 📋 Recommended Actions
# MAGIC
# MAGIC #### **Immediate Actions** (Critical Priority)
# MAGIC 1. **Check Source Data**: Verify if transaction counts exist in the source USASpending.gov data
# MAGIC 2. **Review ETL Pipeline**: Examine the data ingestion code that loads `usaspending_state_quarter_gold` and `usaspending_state_year_gold`
# MAGIC 3. **Identify Missing Logic**: Determine if transaction count aggregation was:
# MAGIC    * Never implemented in the ETL
# MAGIC    * Commented out or removed
# MAGIC    * Failed silently during execution
# MAGIC
# MAGIC #### **Short-Term Actions**
# MAGIC 4. **Regenerate Tables**: Re-run the ETL pipeline with corrected logic to populate `transaction_count`
# MAGIC 5. **Add Data Quality Checks**: Implement validation in the ETL to ensure `transaction_count > 0` when `total_obligations > 0`
# MAGIC 6. **Update Documentation**: Document the expected relationship between obligations and transaction counts
# MAGIC
# MAGIC #### **Long-Term Actions**
# MAGIC 7. **Automated Monitoring**: Schedule this test notebook to run after each data refresh
# MAGIC 8. **ETL Unit Tests**: Add unit tests to verify transaction count aggregation logic
# MAGIC 9. **Dashboard Adjustments**: Remove or hide transaction-based metrics until data is corrected
# MAGIC 10. **Alert System**: Set up alerts if transaction counts drop below expected thresholds
# MAGIC
# MAGIC ### 🔧 Technical Next Steps
# MAGIC
# MAGIC 1. **Locate ETL Code**: Find the notebook/pipeline that creates these gold tables
# MAGIC 2. **Review Aggregation Logic**: Look for `SUM(transaction_count)` or similar aggregations
# MAGIC 3. **Check Source Tables**: Query the bronze/silver layer tables to verify transaction counts exist upstream
# MAGIC 4. **Fix & Backfill**: Correct the ETL logic and backfill historical data
# MAGIC 5. **Validate**: Re-run all data quality tests after regeneration
# MAGIC
# MAGIC ### 💡 Temporary Workaround
# MAGIC
# MAGIC Until the data is corrected, queries should:
# MAGIC * Avoid dividing by `transaction_count` (use `NULLIF(transaction_count, 0)`)
# MAGIC * Hide transaction-based KPIs from dashboards
# MAGIC * Focus analyses on total obligations instead of per-transaction metrics
# MAGIC * Add disclaimer notes where transaction counts are displayed

# COMMAND ----------

# DBTITLE 1,ETL Pipeline Diagnostic Guide
# MAGIC %md
# MAGIC ---
# MAGIC ## 🔧 ETL Pipeline Diagnostic & Remediation Guide
# MAGIC
# MAGIC This section provides step-by-step instructions to diagnose and fix the transaction count issue in your ETL pipeline.
# MAGIC
# MAGIC ### Phase 1: Locate the ETL Pipeline
# MAGIC
# MAGIC Your ETL pipeline likely exists as one of these:
# MAGIC * **Notebook**: A Python or SQL notebook with transformation logic
# MAGIC * **Lakeflow Pipeline (formerly DLT)**: A declarative pipeline definition
# MAGIC * **Databricks Job**: A scheduled workflow
# MAGIC * **Spark Script**: A `.py` or `.scala` file
# MAGIC
# MAGIC **Action**: Search your workspace for notebooks/files containing:
# MAGIC * `usaspending_state_quarter_gold`
# MAGIC * `usaspending_state_year_gold`
# MAGIC * `CREATE TABLE` or `INSERT INTO`

# COMMAND ----------

# DBTITLE 1,Diagnostic Query 1: Find Source Tables
# MAGIC %md
# MAGIC ### Diagnostic Query 1: Find Source Tables
# MAGIC
# MAGIC Identify upstream bronze/silver tables that feed into the gold tables.

# COMMAND ----------

# DBTITLE 1,Find Upstream Tables
# Search for source tables using lineage or table properties
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Check table properties for clues about source
table_details = spark.sql("""
  DESCRIBE EXTENDED default.usaspending_state_quarter_gold
""").collect()

for row in table_details:
    print(f"{row.col_name}: {row.data_type}")

print("\n" + "="*80 + "\n")

# Look for views that might reference source tables
try:
    view_def = spark.sql("""
      SHOW CREATE TABLE default.usaspending_state_quarter_gold
    """).collect()
    for row in view_def:
        print(row[0])
except Exception as e:
    print(f"Table is not a view: {e}")

# COMMAND ----------

# DBTITLE 1,Diagnostic Query 2: Check Bronze Layer
# MAGIC %md
# MAGIC ### Diagnostic Query 2: Check Bronze/Silver Layer
# MAGIC
# MAGIC Verify if transaction counts exist in upstream tables.

# COMMAND ----------

# DBTITLE 1,List All Tables
# MAGIC %sql
# MAGIC -- Find all tables that might be source data
# MAGIC SHOW TABLES IN default LIKE 'usaspending*'

# COMMAND ----------

# DBTITLE 1,Sample Bronze Data
# MAGIC %sql
# MAGIC -- If you have a bronze layer, check for transaction_count
# MAGIC -- Replace 'usaspending_bronze' with your actual bronze table name
# MAGIC
# MAGIC -- Example: Check if bronze table has transaction counts
# MAGIC SELECT 
# MAGIC   COUNT(*) as total_records,
# MAGIC   COUNT(DISTINCT state) as states,
# MAGIC   SUM(CASE WHEN transaction_count > 0 THEN 1 ELSE 0 END) as records_with_tx_count,
# MAGIC   SUM(transaction_count) as total_transactions,
# MAGIC   AVG(transaction_count) as avg_tx_per_record
# MAGIC FROM default.usaspending_state_quarter_gold  -- Change to bronze table name
# MAGIC LIMIT 1000

# COMMAND ----------

# DBTITLE 1,Common ETL Patterns & Fixes
# MAGIC %md
# MAGIC ---
# MAGIC ### Common ETL Patterns & How to Fix Them
# MAGIC
# MAGIC #### Pattern 1: Missing Aggregation in GROUP BY
# MAGIC
# MAGIC **Problem**: The ETL groups by state/year/quarter but doesn't aggregate transaction_count
# MAGIC
# MAGIC ```sql
# MAGIC -- ❌ WRONG: Missing transaction_count aggregation
# MAGIC CREATE OR REPLACE TABLE usaspending_state_quarter_gold AS
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   SUM(total_obligations) as total_obligations
# MAGIC   -- Missing: SUM(transaction_count) as transaction_count
# MAGIC FROM usaspending_bronze
# MAGIC GROUP BY state, year, quarter;
# MAGIC ```
# MAGIC
# MAGIC ```sql
# MAGIC -- ✅ CORRECT: Include transaction_count aggregation
# MAGIC CREATE OR REPLACE TABLE usaspending_state_quarter_gold AS
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   SUM(transaction_count) as transaction_count  -- Fixed!
# MAGIC FROM usaspending_bronze
# MAGIC GROUP BY state, year, quarter;
# MAGIC ```
# MAGIC
# MAGIC #### Pattern 2: Column Not in Source
# MAGIC
# MAGIC **Problem**: The bronze/silver table doesn't have transaction_count column
# MAGIC
# MAGIC **Solution**: 
# MAGIC 1. Check if source data has transaction counts
# MAGIC 2. If yes, trace back through medallion layers to find where it was dropped
# MAGIC 3. If no, calculate it from transaction-level data:
# MAGIC
# MAGIC ```sql
# MAGIC -- Count individual transactions if you have transaction-level data
# MAGIC CREATE OR REPLACE TABLE usaspending_state_quarter_gold AS
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   SUM(obligation_amount) as total_obligations,
# MAGIC   COUNT(*) as transaction_count  -- Count rows to get transaction count
# MAGIC FROM usaspending_transactions  -- Transaction-level table
# MAGIC GROUP BY state, year, quarter;
# MAGIC ```
# MAGIC
# MAGIC #### Pattern 3: Hardcoded Zero or NULL
# MAGIC
# MAGIC **Problem**: ETL explicitly sets transaction_count to 0 or NULL
# MAGIC
# MAGIC ```sql
# MAGIC -- ❌ WRONG: Hardcoded zero
# MAGIC CREATE OR REPLACE TABLE usaspending_state_quarter_gold AS
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   0 as transaction_count  -- Wrong!
# MAGIC FROM usaspending_bronze
# MAGIC GROUP BY state, year, quarter;
# MAGIC ```
# MAGIC
# MAGIC **Fix**: Remove the hardcoded value and aggregate properly
# MAGIC
# MAGIC #### Pattern 4: Using SELECT * Without transaction_count
# MAGIC
# MAGIC **Problem**: Using SELECT * from a view/subquery that doesn't include transaction_count
# MAGIC
# MAGIC ```sql
# MAGIC -- ❌ WRONG: Source view doesn't have transaction_count
# MAGIC CREATE OR REPLACE TABLE usaspending_state_quarter_gold AS
# MAGIC SELECT *  -- If source doesn't have transaction_count, this won't add it
# MAGIC FROM (
# MAGIC   SELECT state, year, quarter, SUM(total_obligations) as total_obligations
# MAGIC   FROM usaspending_bronze
# MAGIC   GROUP BY state, year, quarter
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC **Fix**: Explicitly add transaction_count to the subquery

# COMMAND ----------

# DBTITLE 1,Step-by-Step Fix Procedure
# MAGIC %md
# MAGIC ---
# MAGIC ### Step-by-Step Fix Procedure
# MAGIC
# MAGIC #### Step 1: Create a Test Query
# MAGIC
# MAGIC Before modifying the ETL, test your fix:
# MAGIC
# MAGIC ```sql
# MAGIC -- Test query to verify transaction counts exist in source
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   SUM(transaction_count) as transaction_count,  -- Or COUNT(*) if transaction-level
# MAGIC   SUM(transaction_count) / SUM(total_obligations) as tx_per_dollar
# MAGIC FROM your_source_table  -- Replace with actual source
# MAGIC WHERE state IN ('CA', 'TX', 'NY')  -- Test with sample states
# MAGIC   AND year = 2024
# MAGIC   AND quarter = 'Q1'
# MAGIC GROUP BY state, year, quarter
# MAGIC ORDER BY state;
# MAGIC ```
# MAGIC
# MAGIC Expected result: `transaction_count` should be > 0
# MAGIC
# MAGIC #### Step 2: Backup Existing Tables
# MAGIC
# MAGIC ```sql
# MAGIC -- Create backup before modifying
# MAGIC CREATE TABLE default.usaspending_state_quarter_gold_backup AS
# MAGIC SELECT * FROM default.usaspending_state_quarter_gold;
# MAGIC
# MAGIC CREATE TABLE default.usaspending_state_year_gold_backup AS
# MAGIC SELECT * FROM default.usaspending_state_year_gold;
# MAGIC ```
# MAGIC
# MAGIC #### Step 3: Apply the Fix
# MAGIC
# MAGIC Modify your ETL notebook/pipeline to include transaction_count aggregation.
# MAGIC
# MAGIC #### Step 4: Regenerate Gold Tables
# MAGIC
# MAGIC ```sql
# MAGIC -- Drop and recreate (or use CREATE OR REPLACE)
# MAGIC DROP TABLE IF EXISTS default.usaspending_state_quarter_gold;
# MAGIC
# MAGIC CREATE TABLE default.usaspending_state_quarter_gold AS
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   period,
# MAGIC   country,
# MAGIC   country_code,
# MAGIC   geo_level,
# MAGIC   SUM(total_obligations) as total_obligations,
# MAGIC   SUM(transaction_count) as transaction_count  -- FIXED LINE
# MAGIC FROM your_source_table
# MAGIC GROUP BY state, year, quarter, period, country, country_code, geo_level;
# MAGIC ```
# MAGIC
# MAGIC #### Step 5: Validate the Fix
# MAGIC
# MAGIC Run the data quality tests from this notebook:
# MAGIC
# MAGIC ```python
# MAGIC # Run Test 10 to verify transaction counts are now populated
# MAGIC %run "Cell 37: Test 10: Transaction Counts"
# MAGIC ```
# MAGIC
# MAGIC #### Step 6: Compare Before/After
# MAGIC
# MAGIC ```sql
# MAGIC -- Compare backup vs new table
# MAGIC SELECT 
# MAGIC   'BACKUP' as source,
# MAGIC   COUNT(*) as records,
# MAGIC   SUM(CASE WHEN transaction_count = 0 THEN 1 ELSE 0 END) as zero_count
# MAGIC FROM default.usaspending_state_quarter_gold_backup
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 
# MAGIC   'CURRENT' as source,
# MAGIC   COUNT(*) as records,
# MAGIC   SUM(CASE WHEN transaction_count = 0 THEN 1 ELSE 0 END) as zero_count
# MAGIC FROM default.usaspending_state_quarter_gold;
# MAGIC ```
# MAGIC
# MAGIC Expected: CURRENT should have zero_count = 0

# COMMAND ----------

# DBTITLE 1,Validation Checklist
# MAGIC %md
# MAGIC ---
# MAGIC ### ✅ Post-Fix Validation Checklist
# MAGIC
# MAGIC After fixing the ETL pipeline, verify:
# MAGIC
# MAGIC - [ ] **Row Count Match**: New table has same row count as before (72 quarterly, 18 yearly)
# MAGIC - [ ] **No NULL Transactions**: `transaction_count IS NOT NULL` for all records
# MAGIC - [ ] **No Zero Transactions**: `transaction_count > 0` for records with obligations > 0
# MAGIC - [ ] **Transaction Counts Reasonable**: Average transaction size is within expected range
# MAGIC - [ ] **Aggregation Reconciliation**: Quarterly sums still match yearly aggregations
# MAGIC - [ ] **Total Obligations Unchanged**: Total obligations match backup table
# MAGIC - [ ] **All States Present**: Same 6 states (CA, TX, NY, FL, PA, NJ) still present
# MAGIC - [ ] **All Time Periods Present**: Same time range (2024-Q1 through 2026-Q2)
# MAGIC - [ ] **Data Quality Tests Pass**: Re-run all 10 tests in this notebook
# MAGIC - [ ] **Dashboard Functions**: Test dashboard metrics that use transaction_count
# MAGIC
# MAGIC ### Run Full Validation
# MAGIC
# MAGIC ```python
# MAGIC # Re-run all data quality tests
# MAGIC for test_cell in [
# MAGIC     'b001b3de-573c-4610-95ca-95867a4c69cf',  # Test 1: Row Count
# MAGIC     '3152bcfc-f294-4a9f-aefe-942c891c90b9',  # Test 2: NULL Checks
# MAGIC     '920f0bd0-60b3-4da1-a60d-3de23b8d7394',  # Test 3: Data Types
# MAGIC     # ... add all test cell IDs
# MAGIC ]:
# MAGIC     print(f"Running test: {test_cell}")
# MAGIC     # Run each test cell
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Prevention: Add to ETL Pipeline
# MAGIC %md
# MAGIC ---
# MAGIC ### 🛡️ Prevention: Add to Your ETL Pipeline
# MAGIC
# MAGIC To prevent this issue from happening again, add these checks to your ETL:
# MAGIC
# MAGIC #### 1. Pre-Flight Validation
# MAGIC
# MAGIC Before writing to gold tables, validate the data:
# MAGIC
# MAGIC ```python
# MAGIC # In your ETL notebook/pipeline
# MAGIC from pyspark.sql.functions import col, sum as spark_sum, count
# MAGIC
# MAGIC # Validate before writing
# MAGIC df_to_write = spark.sql("""
# MAGIC   SELECT 
# MAGIC     state, year, quarter,
# MAGIC     SUM(total_obligations) as total_obligations,
# MAGIC     SUM(transaction_count) as transaction_count
# MAGIC   FROM source_table
# MAGIC   GROUP BY state, year, quarter
# MAGIC """)
# MAGIC
# MAGIC # Validation checks
# MAGIC zero_tx_count = df_to_write.filter(col("transaction_count") == 0).count()
# MAGIC if zero_tx_count > 0:
# MAGIC     raise ValueError(f"ERROR: {zero_tx_count} records have zero transaction_count!")
# MAGIC
# MAGIC total_tx = df_to_write.agg(spark_sum("transaction_count")).collect()[0][0]
# MAGIC if total_tx == 0:
# MAGIC     raise ValueError("ERROR: Total transaction_count is zero!")
# MAGIC
# MAGIC print(f"✓ Validation passed: {total_tx:,} total transactions")
# MAGIC
# MAGIC # Write to gold table
# MAGIC df_to_write.write.mode("overwrite").saveAsTable("default.usaspending_state_quarter_gold")
# MAGIC ```
# MAGIC
# MAGIC #### 2. Post-Write Validation
# MAGIC
# MAGIC ```sql
# MAGIC -- Add at the end of your ETL
# MAGIC SELECT 
# MAGIC   CASE 
# MAGIC     WHEN COUNT(*) FILTER (WHERE transaction_count = 0) > 0 
# MAGIC     THEN 'FAIL: Zero transaction counts detected'
# MAGIC     ELSE 'PASS: All records have transaction counts'
# MAGIC   END as validation_status,
# MAGIC   COUNT(*) as total_records,
# MAGIC   COUNT(*) FILTER (WHERE transaction_count = 0) as zero_tx_records,
# MAGIC   SUM(transaction_count) as total_transactions
# MAGIC FROM default.usaspending_state_quarter_gold;
# MAGIC ```
# MAGIC
# MAGIC #### 3. Automated Alerts
# MAGIC
# MAGIC Schedule this test notebook to run after each ETL refresh and set up alerts:
# MAGIC
# MAGIC ```python
# MAGIC # Example: Send alert if test fails
# MAGIC test_result = spark.sql("""
# MAGIC   SELECT COUNT(*) as zero_count
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE transaction_count = 0
# MAGIC """).collect()[0]['zero_count']
# MAGIC
# MAGIC if test_result > 0:
# MAGIC     # Send email/Slack alert
# MAGIC     dbutils.notebook.exit(f"ALERT: {test_result} records with zero transaction_count")
# MAGIC ```
# MAGIC
# MAGIC #### 4. Unit Tests
# MAGIC
# MAGIC Add unit tests to your ETL pipeline:
# MAGIC
# MAGIC ```python
# MAGIC import unittest
# MAGIC
# MAGIC class TestUSASpendingETL(unittest.TestCase):
# MAGIC     
# MAGIC     def test_transaction_count_not_zero(self):
# MAGIC         """Test that all records have transaction_count > 0"""
# MAGIC         df = spark.table("default.usaspending_state_quarter_gold")
# MAGIC         zero_count = df.filter(col("transaction_count") == 0).count()
# MAGIC         self.assertEqual(zero_count, 0, "Found records with zero transaction_count")
# MAGIC     
# MAGIC     def test_transaction_count_not_null(self):
# MAGIC         """Test that transaction_count is never NULL"""
# MAGIC         df = spark.table("default.usaspending_state_quarter_gold")
# MAGIC         null_count = df.filter(col("transaction_count").isNull()).count()
# MAGIC         self.assertEqual(null_count, 0, "Found NULL transaction_count values")
# MAGIC     
# MAGIC     def test_reasonable_avg_transaction_size(self):
# MAGIC         """Test that average transaction size is reasonable"""
# MAGIC         result = spark.sql("""
# MAGIC             SELECT AVG(total_obligations / NULLIF(transaction_count, 0)) as avg_tx_size
# MAGIC             FROM default.usaspending_state_quarter_gold
# MAGIC         """).collect()[0]['avg_tx_size']
# MAGIC         
# MAGIC         # Assuming reasonable range is $1K to $10M per transaction
# MAGIC         self.assertGreater(result, 1000, "Average transaction size too small")
# MAGIC         self.assertLess(result, 10000000, "Average transaction size too large")
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Executive Summary & Action Plan
# MAGIC %md
# MAGIC ---
# MAGIC ## 🎯 Executive Summary & Prioritized Action Plan
# MAGIC
# MAGIC ### Issue Summary
# MAGIC
# MAGIC **Problem**: 100% of records in both gold tables have `transaction_count = 0` despite $1.64T in total obligations
# MAGIC
# MAGIC **Root Cause**: ETL pipeline missing transaction_count aggregation logic
# MAGIC
# MAGIC **Impact**: 
# MAGIC * ❌ Broken: All transaction-based metrics and analysis
# MAGIC * ✅ Working: Total obligations analysis, growth trends, state rankings
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Immediate Actions (Today)
# MAGIC
# MAGIC #### Priority 1: Locate the ETL Pipeline ⏱️ 15 min
# MAGIC
# MAGIC **What to do:**
# MAGIC 1. Search workspace for notebooks containing `usaspending_state_quarter_gold`
# MAGIC 2. Look in Jobs, Workflows, or Pipelines
# MAGIC 3. Check for SQL CREATE TABLE or INSERT statements
# MAGIC
# MAGIC **Query to help:**
# MAGIC ```python
# MAGIC # Search your workspace
# MAGIC %sh find /Workspace -name "*.py" -o -name "*.sql" | xargs grep -l "usaspending_state_quarter_gold" 2>/dev/null
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Priority 2: Identify Source Tables ⏱️ 10 min
# MAGIC
# MAGIC **What to do:**
# MAGIC 1. Run **Diagnostic Query 1** (cell 55 in this notebook)
# MAGIC 2. List all USASpending tables: `SHOW TABLES IN default LIKE 'usaspending*'`
# MAGIC 3. Identify bronze/silver layer tables
# MAGIC
# MAGIC **Expected outcome:** Find the source table(s) that feed the gold layer
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Priority 3: Verify Source Has Transaction Counts ⏱️ 5 min
# MAGIC
# MAGIC **What to do:**
# MAGIC Query your source table:
# MAGIC ```sql
# MAGIC SELECT 
# MAGIC   COUNT(*) as records,
# MAGIC   SUM(transaction_count) as total_transactions,
# MAGIC   AVG(transaction_count) as avg_per_record
# MAGIC FROM your_bronze_or_silver_table
# MAGIC LIMIT 10;
# MAGIC ```
# MAGIC
# MAGIC **Decision point:**
# MAGIC * If `total_transactions > 0`: Source has data → Go to Priority 4
# MAGIC * If `total_transactions = 0`: Source missing data → Trace back further
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Short-Term Actions (This Week)
# MAGIC
# MAGIC #### Priority 4: Fix the ETL Code ⏱️ 30 min
# MAGIC
# MAGIC **What to do:**
# MAGIC 1. Open your ETL notebook/pipeline
# MAGIC 2. Find the SELECT statement that creates the gold table
# MAGIC 3. Add `SUM(transaction_count) as transaction_count` to the aggregation
# MAGIC 4. Review **Common ETL Patterns & Fixes** (cell 58 in this notebook)
# MAGIC
# MAGIC **Example fix:**
# MAGIC ```sql
# MAGIC -- Add this line to your ETL
# MAGIC SUM(transaction_count) as transaction_count  -- ← ADD THIS
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Priority 5: Test & Validate ⏱️ 20 min
# MAGIC
# MAGIC **What to do:**
# MAGIC 1. Run **Step 1: Create a Test Query** (cell 59) on sample data
# MAGIC 2. Create backups: **Step 2: Backup Existing Tables**
# MAGIC 3. Apply fix: **Step 3: Apply the Fix**
# MAGIC 4. Regenerate: **Step 4: Regenerate Gold Tables**
# MAGIC 5. Validate: **Step 5: Validate the Fix**
# MAGIC
# MAGIC **Success criteria:**
# MAGIC * All 72 quarterly records have `transaction_count > 0`
# MAGIC * Test 10 passes (0 records with zero transaction_count)
# MAGIC * Total obligations unchanged from backup
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Priority 6: Update Dashboard ⏱️ 15 min
# MAGIC
# MAGIC **What to do:**
# MAGIC 1. Re-test all dashboard queries that use `transaction_count`
# MAGIC 2. Remove any temporary workarounds (NULLIF, disclaimers)
# MAGIC 3. Re-enable transaction-based KPIs
# MAGIC 4. Refresh dashboard to pull new data
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Long-Term Actions (Next 2 Weeks)
# MAGIC
# MAGIC #### Priority 7: Add Automated Monitoring ⏱️ 1 hour
# MAGIC
# MAGIC **What to do:**
# MAGIC 1. Schedule this test notebook to run after each ETL refresh
# MAGIC 2. Set up email/Slack alerts for test failures
# MAGIC 3. Add monitoring dashboard for data quality metrics
# MAGIC
# MAGIC **Tools:**
# MAGIC * Databricks Jobs - Schedule notebook runs
# MAGIC * Databricks Alerts - Notify on failures
# MAGIC * Dashboard - Display test results over time
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Priority 8: Prevent Future Issues ⏱️ 2 hours
# MAGIC
# MAGIC **What to do:**
# MAGIC 1. Add pre-flight validation to ETL (cell 62: Prevention section)
# MAGIC 2. Implement unit tests (cell 62: Unit Tests section)
# MAGIC 3. Document expected data quality standards
# MAGIC 4. Add validation to CI/CD pipeline if applicable
# MAGIC
# MAGIC **Code to add:**
# MAGIC ```python
# MAGIC # Add to your ETL before writing gold table
# MAGIC if df.filter(col("transaction_count") == 0).count() > 0:
# MAGIC     raise ValueError("Transaction count validation failed!")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Resource Estimates
# MAGIC
# MAGIC | Phase | Time | Complexity | Dependencies |
# MAGIC |-------|------|------------|-------------|
# MAGIC | Diagnosis (P1-P3) | 30 min | Low | None |
# MAGIC | Fix & Test (P4-P5) | 50 min | Medium | Access to ETL code |
# MAGIC | Dashboard Update (P6) | 15 min | Low | Fixed data |
# MAGIC | **Total (Immediate)** | **1.5 hours** | | |
# MAGIC | Monitoring (P7) | 1 hour | Medium | Databricks Jobs access |
# MAGIC | Prevention (P8) | 2 hours | Medium | ETL code access |
# MAGIC | **Total (Complete)** | **4.5 hours** | | |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Success Criteria
# MAGIC
# MAGIC ✅ **Fix is successful when:**
# MAGIC 1. All 10 data quality tests pass
# MAGIC 2. Zero records with `transaction_count = 0`
# MAGIC 3. Total obligations match backup
# MAGIC 4. Dashboard metrics work correctly
# MAGIC 5. Automated monitoring is active
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Next Steps - Start Here
# MAGIC
# MAGIC **Right Now:**
# MAGIC 1. 🔍 Run **cell 55** (Find Upstream Tables) to locate your ETL
# MAGIC 2. 🔍 Run **cell 57** (List All Tables) to see available tables
# MAGIC 3. 📝 Document what you find
# MAGIC
# MAGIC **Then:**
# MAGIC 4. Follow the Immediate Actions (Priority 1-3) above
# MAGIC 5. Schedule time this week for Short-Term Actions (Priority 4-6)
# MAGIC 6. Plan for Long-Term Actions (Priority 7-8) in next sprint
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Questions? Start with These
# MAGIC
# MAGIC **Q: I can't find the ETL pipeline**
# MAGIC * A: Check Workflows/Jobs, or search for notebooks with `CREATE TABLE` statements
# MAGIC
# MAGIC **Q: Source table doesn't have transaction_count**
# MAGIC * A: You may need transaction-level data - use `COUNT(*)` when aggregating transactions
# MAGIC
# MAGIC **Q: How do I know if my fix worked?**
# MAGIC * A: Run Test 10 (cell 37) - it should show 0 records with zero transaction_count
# MAGIC
# MAGIC **Q: Can I fix this without disrupting the dashboard?**
# MAGIC * A: Yes - create backup tables first, test thoroughly, then swap atomically
# MAGIC
# MAGIC **Q: What if I break something?**
# MAGIC * A: That's why we backup first! You can restore from `usaspending_state_quarter_gold_backup`
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Contact & Escalation
# MAGIC
# MAGIC If you need help:
# MAGIC 1. Review the **Common ETL Patterns & Fixes** (cell 58)
# MAGIC 2. Review the **Step-by-Step Fix Procedure** (cell 59)
# MAGIC 3. Run diagnostic queries in cells 55-57
# MAGIC 4. Escalate to your data engineering team with this notebook
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Good luck! You've got this! 🚀**

# COMMAND ----------

# DBTITLE 1,Query 1: Moving Averages
# MAGIC %md
# MAGIC ### Advanced Query 1: Moving Averages and Trends
# MAGIC
# MAGIC Calculates 3-quarter and 12-quarter (3-year) moving averages for each state. Useful for smoothing seasonal variations and identifying long-term trends.

# COMMAND ----------

# DBTITLE 1,Moving Averages
# MAGIC %sql
# MAGIC -- Moving averages and trend analysis
# MAGIC WITH quarterly_data AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     year,
# MAGIC     quarter,
# MAGIC     period,
# MAGIC     SUM(total_obligations) as obligations
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state, year, quarter, period
# MAGIC )
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   period,
# MAGIC   obligations as current_obligations,
# MAGIC   ROUND(AVG(obligations) OVER (
# MAGIC     PARTITION BY state 
# MAGIC     ORDER BY year, quarter 
# MAGIC     ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
# MAGIC   ), 2) as moving_avg_3q,
# MAGIC   ROUND(AVG(obligations) OVER (
# MAGIC     PARTITION BY state 
# MAGIC     ORDER BY year, quarter 
# MAGIC     ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
# MAGIC   ), 2) as moving_avg_12q,
# MAGIC   ROUND(obligations - AVG(obligations) OVER (
# MAGIC     PARTITION BY state 
# MAGIC     ORDER BY year, quarter 
# MAGIC     ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
# MAGIC   ), 2) as deviation_from_3q_avg
# MAGIC FROM quarterly_data
# MAGIC ORDER BY state, year, quarter

# COMMAND ----------

# DBTITLE 1,Query 2: Statistical Analysis
# MAGIC %md
# MAGIC ### Advanced Query 2: Statistical Analysis by State
# MAGIC
# MAGIC Provides comprehensive statistical measures including percentiles, standard deviation, coefficient of variation, and distribution metrics.

# COMMAND ----------

# DBTITLE 1,Statistical Analysis
# MAGIC %sql
# MAGIC -- Statistical analysis: Percentiles, standard deviation, variance
# MAGIC WITH state_stats AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     COUNT(*) as quarter_count,
# MAGIC     SUM(total_obligations) as total_obligations,
# MAGIC     AVG(total_obligations) as avg_obligations,
# MAGIC     STDDEV(total_obligations) as stddev_obligations,
# MAGIC     MIN(total_obligations) as min_obligations,
# MAGIC     MAX(total_obligations) as max_obligations,
# MAGIC     PERCENTILE(total_obligations, 0.25) as p25_obligations,
# MAGIC     PERCENTILE(total_obligations, 0.50) as median_obligations,
# MAGIC     PERCENTILE(total_obligations, 0.75) as p75_obligations,
# MAGIC     PERCENTILE(total_obligations, 0.90) as p90_obligations
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state
# MAGIC )
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   quarter_count,
# MAGIC   ROUND(total_obligations, 2) as total_obligations,
# MAGIC   ROUND(avg_obligations, 2) as avg_obligations,
# MAGIC   ROUND(stddev_obligations, 2) as stddev_obligations,
# MAGIC   ROUND(stddev_obligations / NULLIF(avg_obligations, 0), 3) as coefficient_of_variation,
# MAGIC   ROUND(min_obligations, 2) as min_obligations,
# MAGIC   ROUND(p25_obligations, 2) as p25_obligations,
# MAGIC   ROUND(median_obligations, 2) as median_obligations,
# MAGIC   ROUND(p75_obligations, 2) as p75_obligations,
# MAGIC   ROUND(p90_obligations, 2) as p90_obligations,
# MAGIC   ROUND(max_obligations, 2) as max_obligations,
# MAGIC   ROUND(max_obligations - min_obligations, 2) as range_obligations
# MAGIC FROM state_stats
# MAGIC ORDER BY total_obligations DESC

# COMMAND ----------

# DBTITLE 1,Query 3: Seasonal Pattern Detection
# MAGIC %md
# MAGIC ### Advanced Query 3: Seasonal Pattern Detection
# MAGIC
# MAGIC Analyzes spending patterns by quarter across all years to identify seasonal trends. Shows average, min, max, and variance for each quarter.

# COMMAND ----------

# DBTITLE 1,Seasonal Patterns
# MAGIC %sql
# MAGIC -- Seasonal pattern detection by quarter
# MAGIC WITH quarterly_patterns AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     quarter,
# MAGIC     SUM(total_obligations) as total_obligations,
# MAGIC     AVG(total_obligations) as avg_obligations,
# MAGIC     STDDEV(total_obligations) as stddev_obligations,
# MAGIC     MIN(total_obligations) as min_obligations,
# MAGIC     MAX(total_obligations) as max_obligations,
# MAGIC     COUNT(*) as year_count
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state, quarter
# MAGIC ),
# MAGIC total_by_state AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     SUM(total_obligations) as state_total
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state
# MAGIC )
# MAGIC SELECT 
# MAGIC   qp.state,
# MAGIC   qp.quarter,
# MAGIC   ROUND(qp.total_obligations, 2) as total_obligations,
# MAGIC   ROUND(qp.avg_obligations, 2) as avg_obligations,
# MAGIC   ROUND(qp.stddev_obligations, 2) as stddev_obligations,
# MAGIC   ROUND(qp.min_obligations, 2) as min_obligations,
# MAGIC   ROUND(qp.max_obligations, 2) as max_obligations,
# MAGIC   qp.year_count,
# MAGIC   ROUND((qp.total_obligations / ts.state_total) * 100, 2) as pct_of_state_total,
# MAGIC   CASE 
# MAGIC     WHEN qp.quarter = 1 THEN 'Q1 - Jan-Mar'
# MAGIC     WHEN qp.quarter = 2 THEN 'Q2 - Apr-Jun'
# MAGIC     WHEN qp.quarter = 3 THEN 'Q3 - Jul-Sep'
# MAGIC     WHEN qp.quarter = 4 THEN 'Q4 - Oct-Dec'
# MAGIC   END as quarter_name
# MAGIC FROM quarterly_patterns qp
# MAGIC JOIN total_by_state ts ON qp.state = ts.state
# MAGIC ORDER BY qp.state, qp.quarter

# COMMAND ----------

# DBTITLE 1,Query 4: Growth Rate Analysis
# MAGIC %md
# MAGIC ### Advanced Query 4: Comprehensive Growth Rate Analysis
# MAGIC
# MAGIC Combines multiple growth metrics using LAG and LEAD window functions: quarter-over-quarter, year-over-year, and forward-looking next quarter predictions.

# COMMAND ----------

# DBTITLE 1,Growth Rate Analysis
# MAGIC %sql
# MAGIC -- Comprehensive growth rate analysis with LAG/LEAD
# MAGIC WITH quarterly_data AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     year,
# MAGIC     quarter,
# MAGIC     period,
# MAGIC     SUM(total_obligations) as obligations,
# MAGIC     SUM(transaction_count) as transactions
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state, year, quarter, period
# MAGIC )
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   period,
# MAGIC   obligations as current_obligations,
# MAGIC   transactions as current_transactions,
# MAGIC   
# MAGIC   -- Previous quarter (QoQ)
# MAGIC   LAG(obligations, 1) OVER (PARTITION BY state ORDER BY year, quarter) as prev_quarter_obligations,
# MAGIC   ROUND(
# MAGIC     ((obligations - LAG(obligations, 1) OVER (PARTITION BY state ORDER BY year, quarter)) 
# MAGIC     / NULLIF(LAG(obligations, 1) OVER (PARTITION BY state ORDER BY year, quarter), 0)) * 100, 
# MAGIC     2
# MAGIC   ) as qoq_growth_pct,
# MAGIC   
# MAGIC   -- Same quarter last year (YoY)
# MAGIC   LAG(obligations, 4) OVER (PARTITION BY state ORDER BY year, quarter) as same_quarter_last_year,
# MAGIC   ROUND(
# MAGIC     ((obligations - LAG(obligations, 4) OVER (PARTITION BY state ORDER BY year, quarter)) 
# MAGIC     / NULLIF(LAG(obligations, 4) OVER (PARTITION BY state ORDER BY year, quarter), 0)) * 100, 
# MAGIC     2
# MAGIC   ) as yoy_growth_pct,
# MAGIC   
# MAGIC   -- Next quarter (forward looking)
# MAGIC   LEAD(obligations, 1) OVER (PARTITION BY state ORDER BY year, quarter) as next_quarter_obligations,
# MAGIC   ROUND(
# MAGIC     ((LEAD(obligations, 1) OVER (PARTITION BY state ORDER BY year, quarter) - obligations) 
# MAGIC     / NULLIF(obligations, 0)) * 100, 
# MAGIC     2
# MAGIC   ) as forward_qoq_growth_pct,
# MAGIC   
# MAGIC   -- Cumulative sum
# MAGIC   SUM(obligations) OVER (PARTITION BY state ORDER BY year, quarter ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as cumulative_obligations
# MAGIC   
# MAGIC FROM quarterly_data
# MAGIC ORDER BY state, year, quarter

# COMMAND ----------

# DBTITLE 1,Query 5: Comparative State Rankings
# MAGIC %md
# MAGIC ### Advanced Query 5: Comparative State Rankings Over Time
# MAGIC
# MAGIC Tracks how states rank against each other over time. Shows rank changes and identifies states that are gaining or losing relative position.

# COMMAND ----------

# DBTITLE 1,State Rankings Over Time
# MAGIC %sql
# MAGIC -- State rankings over time with rank changes
# MAGIC WITH quarterly_rankings AS (
# MAGIC   SELECT 
# MAGIC     state,
# MAGIC     year,
# MAGIC     quarter,
# MAGIC     period,
# MAGIC     SUM(total_obligations) as obligations,
# MAGIC     RANK() OVER (PARTITION BY year, quarter ORDER BY SUM(total_obligations) DESC) as rank_in_quarter,
# MAGIC     COUNT(DISTINCT state) OVER (PARTITION BY year, quarter) as total_states
# MAGIC   FROM default.usaspending_state_quarter_gold
# MAGIC   WHERE state IS NOT NULL
# MAGIC   GROUP BY state, year, quarter, period
# MAGIC )
# MAGIC SELECT 
# MAGIC   state,
# MAGIC   year,
# MAGIC   quarter,
# MAGIC   period,
# MAGIC   ROUND(obligations, 2) as obligations,
# MAGIC   rank_in_quarter,
# MAGIC   total_states,
# MAGIC   LAG(rank_in_quarter, 1) OVER (PARTITION BY state ORDER BY year, quarter) as prev_quarter_rank,
# MAGIC   LAG(rank_in_quarter, 1) OVER (PARTITION BY state ORDER BY year, quarter) - rank_in_quarter as rank_change,
# MAGIC   CASE 
# MAGIC     WHEN LAG(rank_in_quarter, 1) OVER (PARTITION BY state ORDER BY year, quarter) - rank_in_quarter > 0 THEN 'Improved'
# MAGIC     WHEN LAG(rank_in_quarter, 1) OVER (PARTITION BY state ORDER BY year, quarter) - rank_in_quarter < 0 THEN 'Declined'
# MAGIC     WHEN LAG(rank_in_quarter, 1) OVER (PARTITION BY state ORDER BY year, quarter) - rank_in_quarter = 0 THEN 'Unchanged'
# MAGIC     ELSE 'First Period'
# MAGIC   END as rank_trend
# MAGIC FROM quarterly_rankings
# MAGIC ORDER BY year DESC, quarter DESC, rank_in_quarter

# COMMAND ----------

# DBTITLE 1,Summary and Next Steps
# MAGIC %md
# MAGIC ---
# MAGIC ## Summary and Next Steps
# MAGIC
# MAGIC This notebook contains:
# MAGIC * **7 Core Data Queries** - Essential metrics for the dashboard
# MAGIC * **10 Data Quality Tests** - Comprehensive validation suite
# MAGIC * **5 Advanced Analytics Queries** - Statistical analysis and trends
# MAGIC
# MAGIC ### Usage
# MAGIC 1. Run all queries to validate data quality
# MAGIC 2. Review any FAIL or WARNING statuses in the test queries
# MAGIC 3. Use core queries as templates for dashboard datasets
# MAGIC 4. Leverage advanced queries for deeper insights
# MAGIC
# MAGIC ### Running the Tests
# MAGIC To run all tests at once, execute all cells in Section 2. Each test returns:
# MAGIC * **PASS** - Test passed successfully
# MAGIC * **WARNING** - Minor issues detected, review recommended
# MAGIC * **FAIL** - Critical issues found, investigation required
# MAGIC
# MAGIC ### Automation
# MAGIC Consider scheduling this notebook to run daily or weekly to monitor data quality over time.