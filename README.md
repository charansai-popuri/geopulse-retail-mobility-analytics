# GeoPulse: Hyper-Local Retail Mobility Analytics

Infotact Solutions internship, Batch-22, Data Analytics (solo project).
Period: 10 Nov 2026 to 10 Dec 2026.

## Problem
Retailers pick store locations from static census data and risk opening a
store that cannibalizes an existing one. GeoPulse uses mobile GPS pings to
measure real foot traffic around store locations.

## Pipeline
Python ping generator -> Snowflake (GEOGRAPHY) -> Apache Sedona spatial joins
-> dbt hourly footfall models -> Kepler.gl map -> Airflow daily runs

## Status
- [x] Week 1: mock GPS ping generator v1 (commuter routine, 1,000 devices)
- [x] Week 1: ping validator v1 (12 quality checks)
- [x] Week 1: scale generator up to millions of pings
- [ ] Week 1: Snowflake setup, GEOGRAPHY tables and data load
- [ ] Week 2: Sedona 500 m catchment joins, dbt hourly unique visitors
- [ ] Mid review: spatial audit and data integrity check
- [ ] Week 3: cannibalization SQL, Kepler.gl map in React
- [ ] Week 4: Airflow automation, 3D H3 hexagons, 24-hour animation
- [ ] Final: report, PPT, demo

## How to run
### 1. Generate mock GPS pings
```
python generator\generate_pings.py
python generator\generate_pings.py --devices 50000 --output data\raw\pings_large.csv
```
The first command makes 1,000 devices (about 60,000 pings). The second makes
50,000 devices (about 3 million pings, 140 MB). Columns: DeviceID, Lat, Long,
Timestamp. CSV files are not committed to Git because `data/raw/` is in `.gitignore`.

### 2. Validate the data
```
python generator\validate_pings.py
python generator\validate_pings.py --file data\raw\pings_large.csv
```
Runs 12 checks and reads the file one row at a time, so it works on millions
of rows. Expected: `12 of 12 checks passed.`