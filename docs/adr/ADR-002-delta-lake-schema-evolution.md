# ADR-002: Delta Lake Schema Evolution Strategy

## Status
Accepted

## Context
The analytical schema evolved significantly after initial implementation.

New enterprise requirements introduced:
- country
- country_code
- geo_level
- source_system
- future GIS attributes
- future multi-country fields

Traditional overwrite operations caused schema mismatch failures.

## Decision
Use Delta Lake schema evolution with controlled overwrite strategies.

## Implemented Strategy
Primary approach:

```python
.option("overwriteSchema", "true")
```

Future selective evolution:

```python
.option("mergeSchema", "true")
```

## Rationale
Delta Lake schema evolution supports:
- controlled metadata evolution
- additive enterprise attributes
- governance continuity
- backward compatibility

## Consequences
### Positive
- flexible enterprise expansion
- stable governance
- simplified migrations
- future GIS extensibility

### Risks
- uncontrolled schema growth
- inconsistent metadata if unmanaged
- accidental schema drift

## Governance Controls
- all schema changes documented
- ADR updates required
- semantic dataset validation required
- dashboard compatibility validation required