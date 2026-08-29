# Person 2 - Best Track Data Pipeline

**Contributor:** Tisha Biswas (Person 2)

This folder contains work for Module 1 (Data Pipeline), Person 2 responsibility: 
downloading, filtering, and cleaning IBTrACS Best Track data for the North Indian Ocean basin (2013-2021).

## Files
- `data/raw/best_track_raw.csv` - Filtered raw IBTrACS data (NI basin, 2013-2021), all original columns.
- `data/clean/best_track_clean.csv` - Cleaned dataset with 9 columns: storm_id, storm_name, year, timestamp, lat, lon, wind_speed, pressure, category.
- `notebooks/person2_worklog.ipynb` - Full working notebook showing all steps: download, filter, inspect, clean.

## Notes
- Category and wind/pressure sourced from NEWDELHI (IMD) columns, since they are more complete than WMO for this basin.
- Missing values (~19-21% in wind_speed, pressure, category) are kept as NaN, not dropped.

---
*Prepared by Tisha Biswas as part of the CycloCast team, Module 1 - Person 2 (Data Pipeline).*
