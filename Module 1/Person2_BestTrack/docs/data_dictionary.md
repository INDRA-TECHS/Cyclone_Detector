# Data Dictionary — best_track_clean.csv

**Prepared by:** Tisha Biswas (Module 1)
**Source:** IBTrACS v04r01, filtered to North Indian Ocean basin, 2013–2021
**Rows:** 3,415 | **Columns:** 9

| Column       | Data Type      | Description                                                | Notes |
|--------------|---------------|--------------------------------------------------------------|-------|
| storm_id     | text (string)  | Unique ID per storm (IBTrACS SID)                            | No missing values |
| storm_name   | text (string)  | Name of the storm (e.g., "AMPHAN"); may be "UNNAMED"          | No missing values |
| year         | integer        | Season/year of the storm                                     | No missing values |
| timestamp    | datetime       | Exact date & time of observation (format: YYYY-MM-DD HH:MM:SS) | No missing values |
| lat          | float          | Latitude of storm center (degrees north)                     | No missing values |
| lon          | float          | Longitude of storm center (degrees east)                     | No missing values |
| wind_speed   | float          | Sustained wind speed (knots), sourced from NEWDELHI (IMD)     | ~19% missing (NaN) |
| pressure     | float          | Central pressure (millibars), sourced from NEWDELHI (IMD)     | ~20% missing (NaN) |
| category     | text (string)  | IMD storm grade: D, DD, CS, SCS, VSCS, ESCS, SuCS              | ~19% missing (NaN) |

## Key decisions made
- Used **NEWDELHI (IMD)** agency columns instead of WMO/USA, since NEWDELHI had better data completeness for this basin/period.
- Missing values in wind_speed, pressure, and category were **kept as NaN**, not dropped — preserves full storm history; downstream teams can decide how to handle gaps.
- The original IBTrACS units-row (row 0 of the raw file) was removed during cleaning, since it contained text labels instead of real data.

## Category code meanings (IMD grades)
- D = Depression
- DD = Deep Depression
- CS = Cyclonic Storm
- SCS = Severe Cyclonic Storm
- VSCS = Very Severe Cyclonic Storm
- ESCS = Extremely Severe Cyclonic Storm
- SuCS = Super Cyclonic Storm
