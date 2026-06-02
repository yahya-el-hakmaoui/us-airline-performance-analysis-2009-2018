# DECISIONS - Schema audit and consolidation

## Columns removed or renamed
- No business column is renamed at this stage.
- No core operational column is dropped by default.
- The only schema adjustment identified in the audit is a type normalization for `CRS_DEP_TIME` and `CRS_ARR_TIME` in `2012.csv`.

## Missing values
- Keep systematic missing values as nulls in the raw-to-curated path.
- For delay sub-components such as `CARRIER_DELAY`, `WEATHER_DELAY`, `NAS_DELAY`, `SECURITY_DELAY`, and `LATE_AIRCRAFT_DELAY`, treat null as "not reported" rather than as zero.
- Do not impute values during the audit layer.

## Merge strategy
- Keep the intersection of the useful columns present in all years.
- Add a `YEAR` column after loading each file.
- Do not add advanced fusion columns or seasonality-derived columns in this layer.
- Standardize `CRS_DEP_TIME` and `CRS_ARR_TIME` to `Int64` so the 2012 schema matches the reference pattern.

## Notes from the audit
- All 10 yearly CSV files expose the same 28 columns.
- The only schema divergence detected versus 2015 is in `2012.csv` for `CRS_DEP_TIME` and `CRS_ARR_TIME`.
