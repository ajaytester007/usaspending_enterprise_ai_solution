# Multi-Country Expansion
## USASpending Enterprise AI Medallion Solution

## Purpose
Defines roadmap for global public-spend analytics.

## Target Countries
United States, India, United Kingdom, Russia, Mexico, Brazil, Italy, France, Switzerland, Canada, Bangladesh, Pakistan, China, Japan, Singapore, Malaysia, South Africa, Nigeria, Libya, Ethiopia.

## Challenge
Each country differs by API maturity, geography model, currency, fiscal year, language, and source reliability.

## Connector Registry
```text
country_code
country_name
source_system
source_url
access_method
auth_required
data_format
supported_geo_levels
currency
refresh_frequency
owner
status
```

## Canonical Silver Schema
```text
country
country_code
geo_level
admin_level_1
admin_level_2
admin_level_3
postal_code
year
quarter
period
amount
amount_usd
currency
transaction_count
source_system
load_timestamp
```

## Build Order
1. USA
2. Canada
3. UK
4. India
5. France
6. Italy
7. Brazil
8. Mexico
9. Japan
10. Singapore

## Dashboard Filters
- country
- country_code
- geo_level
- year
- period
- currency
