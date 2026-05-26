# Delta Lake Schema Evolution

## Objectives
Enable scalable schema evolution without operational disruption.

## Recommended Columns
- country
- country_code
- geo_level
- zipcode
- district
- latitude
- longitude

## Delta Features
- ACID transactions
- schema evolution
- schema enforcement
- rollback
- time travel

## Recommended Practices
Use:
- overwriteSchema
- mergeSchema
carefully during migrations.